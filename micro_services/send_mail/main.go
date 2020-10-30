package main

import (
	"encoding/json"
	"fmt"
	"os"
	"os/signal"
	"syscall"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"

	_ "github.com/joho/godotenv/autoload"
)

type KafkaMessage struct {
	OrderId int `json:"pay_order_id"`
}

func main() {
	dbUrl := fmt.Sprintf("%v:%v@tcp(%v:%v)/%v?&parseTime=True",
		os.Getenv("DB_USER"), os.Getenv("DB_PASSWORD"), os.Getenv("DB_HOST"), os.Getenv("DB_PORT"), os.Getenv("DB_NAME"),
	)
	db, err := gorm.Open(mysql.Open(dbUrl), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}

	config := &kafka.ConfigMap{
		"metadata.broker.list":            os.Getenv("KAFKA_BROKER"),
		"security.protocol":               "SASL_SSL",
		"sasl.mechanisms":                 "SCRAM-SHA-256",
		"sasl.username":                   os.Getenv("KAFKA_USERNAME"),
		"sasl.password":                   os.Getenv("KAFKA_PASSWORD"),
		"group.id":                        "send-mail-service",
		"go.events.channel.enable":        true,
		"go.application.rebalance.enable": true,
		"default.topic.config":            kafka.ConfigMap{"auto.offset.reset": "latest"},
		//"debug":                           "generic,broker,security",
	}

	// Create kafka consumer
	c, err := kafka.NewConsumer(config)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to create consumer: %s\n", err)
		os.Exit(1)
	}
	fmt.Printf("Created Consumer %v\n", c)

	kafkaTopic := "qgibvd2o-default"
	err = c.Subscribe(kafkaTopic, nil)

	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)
	run := true
	counter := 0
	commitAfter := 1000
	for run == true {
		select {
		case sig := <-sigchan:
			fmt.Printf("Caught signal %v: terminating\n", sig)
			run = false
		case ev := <-c.Events():
			switch e := ev.(type) {
			case kafka.AssignedPartitions:
				c.Assign(e.Partitions)
			case kafka.RevokedPartitions:
				c.Unassign()
			case *kafka.Message:
				fmt.Printf("%% Message on %s: %s\n", e.TopicPartition, string(e.Value))

				var msg KafkaMessage
				json.Unmarshal(e.Value, &msg)

				// fmt.Println(db, msg.OrderId)
				sendMail(db, msg.OrderId)

				counter++
				if counter > commitAfter {
					c.Commit()
					counter = 0
				}
			case kafka.PartitionEOF:
				fmt.Printf("%% Reached %v\n", e)
			case kafka.Error:
				fmt.Fprintf(os.Stderr, "%% Error: %v\n", e)
				run = false
			}
		}
	}
	fmt.Printf("Closing consumer\n")
	c.Close()
}
