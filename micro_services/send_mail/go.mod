module sendmail

go 1.15

require (
	github.com/confluentinc/confluent-kafka-go v1.4.2
	github.com/joho/godotenv v1.3.0
	gopkg.in/alexcesaro/quotedprintable.v3 v3.0.0-20150716171945-2caba252f4dc // indirect
	gopkg.in/gomail.v2 v2.0.0-20160411212932-81ebce5c23df
	gorm.io/driver/mysql v1.0.3
	gorm.io/gorm v1.20.5
	internal/model v0.0.1
)

replace internal/model => ./internal/model
