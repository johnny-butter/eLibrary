package main

import (
	"bytes"
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
		md := MailData{
			order.User.Username,
			shopHistory.TransactionID,
			shopHistory.TransactionTotalPrice,
			shopHistory.TransactionCurrency,
			orderDetails,
		}
		content := renderMail(md)

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
