package model

import (
	"database/sql"
	"time"

	"github.com/guregu/null"
	"github.com/satori/go.uuid"
)

var (
	_ = time.Second
	_ = sql.LevelDefault
	_ = null.Bool{}
	_ = uuid.UUID{}
)

/*
DB Table Details
-------------------------------------


CREATE TABLE `shop_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `transaction_id` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `transaction_total_price` decimal(10,3) NOT NULL,
  `transaction_currency` varchar(5) COLLATE utf8_unicode_ci NOT NULL,
  `transaction_pay_type` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `pay_order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_histor_pay_ord_69c79d_idx` (`pay_order_id`),
  CONSTRAINT `shop_history_pay_order_id_8a46e732_fk_pay_order_id` FOREIGN KEY (`pay_order_id`) REFERENCES `pay_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

JSON Sample
-------------------------------------
{    "create_date": "2260-07-13T20:37:48.43454918+08:00",    "pay_order_id": 51,    "id": 0,    "transaction_id": "vDghWkqLqoLFYGTYehLSyCgeS",    "transaction_total_price": 0.27633576299432533,    "transaction_currency": "ZGShIHtfZxqoMBEUSpanWikaC",    "transaction_pay_type": "XqLejHYTHaJUcqUauPPELkJEg"}



*/

// ShopHistory struct is a row record of the shop_history table in the dk0fw2stwwcn00cc database
type ShopHistory struct {
	//[ 0] id                                             int                  null: false  primary: true   isArray: false  auto: true   col: int             len: -1      default: []
	ID int32
	//[ 1] transaction_id                                 varchar(30)          null: false  primary: false  isArray: false  auto: false  col: varchar         len: 30      default: []
	TransactionID string
	//[ 2] transaction_total_price                        decimal              null: false  primary: false  isArray: false  auto: false  col: decimal         len: -1      default: []
	TransactionTotalPrice float64
	//[ 3] transaction_currency                           varchar(5)           null: false  primary: false  isArray: false  auto: false  col: varchar         len: 5       default: []
	TransactionCurrency string
	//[ 4] transaction_pay_type                           varchar(15)          null: false  primary: false  isArray: false  auto: false  col: varchar         len: 15      default: []
	TransactionPayType string
	//[ 5] create_date                                    datetime             null: false  primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	CreateDate time.Time
	//[ 6] pay_order_id                                   int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	PayOrderID int32
}

var shop_historyTableInfo = &TableInfo{
	Name: "shop_history",
	Columns: []*ColumnInfo{

		&ColumnInfo{
			Index:              0,
			Name:               "id",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "int",
			DatabaseTypePretty: "int",
			IsPrimaryKey:       true,
			IsAutoIncrement:    true,
			IsArray:            false,
			ColumnType:         "int",
			ColumnLength:       -1,
			GoFieldName:        "ID",
			GoFieldType:        "int32",
			JSONFieldName:      "id",
			ProtobufFieldName:  "id",
			ProtobufType:       "int32",
			ProtobufPos:        1,
		},

		&ColumnInfo{
			Index:              1,
			Name:               "transaction_id",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(30)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       30,
			GoFieldName:        "TransactionID",
			GoFieldType:        "string",
			JSONFieldName:      "transaction_id",
			ProtobufFieldName:  "transaction_id",
			ProtobufType:       "string",
			ProtobufPos:        2,
		},

		&ColumnInfo{
			Index:              2,
			Name:               "transaction_total_price",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "decimal",
			DatabaseTypePretty: "decimal",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "decimal",
			ColumnLength:       -1,
			GoFieldName:        "TransactionTotalPrice",
			GoFieldType:        "float64",
			JSONFieldName:      "transaction_total_price",
			ProtobufFieldName:  "transaction_total_price",
			ProtobufType:       "float",
			ProtobufPos:        3,
		},

		&ColumnInfo{
			Index:              3,
			Name:               "transaction_currency",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(5)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       5,
			GoFieldName:        "TransactionCurrency",
			GoFieldType:        "string",
			JSONFieldName:      "transaction_currency",
			ProtobufFieldName:  "transaction_currency",
			ProtobufType:       "string",
			ProtobufPos:        4,
		},

		&ColumnInfo{
			Index:              4,
			Name:               "transaction_pay_type",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(15)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       15,
			GoFieldName:        "TransactionPayType",
			GoFieldType:        "string",
			JSONFieldName:      "transaction_pay_type",
			ProtobufFieldName:  "transaction_pay_type",
			ProtobufType:       "string",
			ProtobufPos:        5,
		},

		&ColumnInfo{
			Index:              5,
			Name:               "create_date",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "datetime",
			DatabaseTypePretty: "datetime",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "datetime",
			ColumnLength:       -1,
			GoFieldName:        "CreateDate",
			GoFieldType:        "time.Time",
			JSONFieldName:      "create_date",
			ProtobufFieldName:  "create_date",
			ProtobufType:       "google.protobuf.Timestamp",
			ProtobufPos:        6,
		},

		&ColumnInfo{
			Index:              6,
			Name:               "pay_order_id",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "int",
			DatabaseTypePretty: "int",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "int",
			ColumnLength:       -1,
			GoFieldName:        "PayOrderID",
			GoFieldType:        "int32",
			JSONFieldName:      "pay_order_id",
			ProtobufFieldName:  "pay_order_id",
			ProtobufType:       "int32",
			ProtobufPos:        7,
		},
	},
}

// TableName sets the insert table name for this struct type
func (s *ShopHistory) TableName() string {
	return "shop_history"
}

// BeforeSave invoked before saving, return an error if field is not populated.
func (s *ShopHistory) BeforeSave() error {
	return nil
}

// Prepare invoked before saving, can be used to populate fields etc.
func (s *ShopHistory) Prepare() {
}

// Validate invoked before performing action, return an error if field is not populated.
func (s *ShopHistory) Validate(action Action) error {
	return nil
}

// TableInfo return table meta data
func (s *ShopHistory) TableInfo() *TableInfo {
	return shop_historyTableInfo
}
