package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"

	"html/template"

	"gopkg.in/gomail.v2"
	"gorm.io/gorm"

	"internal/model"

	_ "github.com/joho/godotenv/autoload"
)

type MailData struct {
	Username              string
	TransactionId         string
	TransactionTotalPrice float64
	TransactionCurrency   string
	OrderDetails          []model.PayOrderDetail
}

// Parse email template
func renderMail(md MailData) string {
	tmpl, err := template.New("template.html").ParseFiles("template.html")
	if err != nil {
		panic(err)
	}

	var content bytes.Buffer
	tmpl.Execute(&content, md)

	return content.String()
}

func getMailContent(
	order model.PayOrder,
	shopHistory model.ShopHistory,
	orderDetails []model.PayOrderDetail,
) (content string) {
	md := MailData{
		order.User.Username,
		shopHistory.TransactionID,
		shopHistory.TransactionTotalPrice,
		shopHistory.TransactionCurrency,
		orderDetails,
	}
	content = renderMail(md)

	return
}

// Send the mail to user
func sendMail(db *gorm.DB, orderId int) {
	// Query DB
	var order model.PayOrder
	var orderDetails []model.PayOrderDetail
	var shopHistory model.ShopHistory

	db.Preload("User").First(&order, orderId)
	db.Preload("Book").Find(&orderDetails, "pay_order_id = ?", orderId)
	db.First(&shopHistory, "pay_order_id = ?", orderId)

	if order.User.Email.Valid {
		content := getMailContent(order, shopHistory, orderDetails)

		// Compose email
		m := gomail.NewMessage()
		m.SetHeader("From", "service@elibrary.com")
		m.SetHeader("To", order.User.Email.String)
		m.SetHeader("Subject", "eLibrary Shopping Record")
		m.SetBody("text/html", content)

		// Send the email
		d := gomail.NewDialer("smtp.gmail.com", 587, os.Getenv("EMAIL_HOST_USER"), os.Getenv("EMAIL_HOST_PASSWORD"))
		if err := d.DialAndSend(m); err != nil {
			panic(err)
		}
	}
}

// Send the mail to user through Trustifi
func sendMailTrustifi(db *gorm.DB, orderId int) {
	// Query DB
	var order model.PayOrder
	var orderDetails []model.PayOrderDetail
	var shopHistory model.ShopHistory

	db.Preload("User").First(&order, orderId)
	db.Preload("Book").Find(&orderDetails, "pay_order_id = ?", orderId)
	db.First(&shopHistory, "pay_order_id = ?", orderId)

	if order.User.Email.Valid {
		var err error

		content := getMailContent(order, shopHistory, orderDetails)

		// Compose email
		url := os.Getenv("TRUSTIFI_URL") + "/api/i/v1/email"

		type u struct {
			Email string `json:"email"`
		}

		reqData := struct {
			Title      string `json:"title"`
			Html       string `json:"html"`
			Recipients []u    `json:"recipients"`
			// From       u      `json:"from"`
		}{
			Title:      "eLibrary Shopping Record",
			Html:       content,
			Recipients: []u{u{order.User.Email.String}},
			// From:       u{"service@elibrary.com"},
		}

		var reqDataJson []byte
		reqDataJson, err = json.Marshal(reqData)
		if err != nil {
			panic(err)
		}

		req, err := http.NewRequest("POST", url, bytes.NewBuffer(reqDataJson))
		req.Header.Add("x-trustifi-key", os.Getenv("TRUSTIFI_KEY"))
		req.Header.Add("x-trustifi-secret", os.Getenv("TRUSTIFI_SECRET"))
		req.Header.Add("Content-Type", "application/json")

		// Send the email
		client := &http.Client{}

		var resp *http.Response
		resp, err = client.Do(req)
		if err != nil {
			panic(err)
		}

		defer resp.Body.Close()
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Println(string(body))
	}
}
