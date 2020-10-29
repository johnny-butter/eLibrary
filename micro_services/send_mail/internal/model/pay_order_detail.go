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


CREATE TABLE `pay_order_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,3) NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `book_id` int(11) NOT NULL,
  `pay_order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pay_order_detail_book_id_00c99834_fk_book_id` (`book_id`),
  KEY `pay_order_d_pay_ord_a22e4a_idx` (`pay_order_id`),
  CONSTRAINT `pay_order_detail_book_id_00c99834_fk_book_id` FOREIGN KEY (`book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `pay_order_detail_pay_order_id_76bfa948_fk_pay_order_id` FOREIGN KEY (`pay_order_id`) REFERENCES `pay_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

JSON Sample
-------------------------------------
{    "create_date": "2088-06-08T14:06:00.570123729+08:00",    "book_id": 99,    "pay_order_id": 98,    "id": 0,    "quantity": 34,    "price": 0.16292510434228244}



*/

// PayOrderDetail struct is a row record of the pay_order_detail table in the dk0fw2stwwcn00cc database
type PayOrderDetail struct {
	//[ 0] id                                             int                  null: false  primary: true   isArray: false  auto: true   col: int             len: -1      default: []
	ID int32 `gorm:"primary_key;AUTO_INCREMENT;column:id;type:int;"`
	//[ 1] quantity                                       int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	Quantity int32 `gorm:"column:quantity;type:int;"`
	//[ 2] price                                          decimal              null: false  primary: false  isArray: false  auto: false  col: decimal         len: -1      default: []
	Price float64 `gorm:"column:price;type:decimal;"`
	//[ 3] create_date                                    datetime             null: false  primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	CreateDate time.Time `gorm:"column:create_date;type:datetime;"`
	//[ 4] book_id                                        int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	BookID int32 `gorm:"column:book_id;type:int;"`
	//[ 5] pay_order_id                                   int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	PayOrderID int32 `gorm:"column:pay_order_id;type:int;"`

	Book Book
}

var pay_order_detailTableInfo = &TableInfo{
	Name: "pay_order_detail",
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
			Name:               "quantity",
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
			GoFieldName:        "Quantity",
			GoFieldType:        "int32",
			JSONFieldName:      "quantity",
			ProtobufFieldName:  "quantity",
			ProtobufType:       "int32",
			ProtobufPos:        2,
		},

		&ColumnInfo{
			Index:              2,
			Name:               "price",
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
			GoFieldName:        "Price",
			GoFieldType:        "float64",
			JSONFieldName:      "price",
			ProtobufFieldName:  "price",
			ProtobufType:       "float",
			ProtobufPos:        3,
		},

		&ColumnInfo{
			Index:              3,
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
			ProtobufPos:        4,
		},

		&ColumnInfo{
			Index:              4,
			Name:               "book_id",
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
			GoFieldName:        "BookID",
			GoFieldType:        "int32",
			JSONFieldName:      "book_id",
			ProtobufFieldName:  "book_id",
			ProtobufType:       "int32",
			ProtobufPos:        5,
		},

		&ColumnInfo{
			Index:              5,
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
			ProtobufPos:        6,
		},
	},
}

// TableName sets the insert table name for this struct type
func (p *PayOrderDetail) TableName() string {
	return "pay_order_detail"
}

// BeforeSave invoked before saving, return an error if field is not populated.
func (p *PayOrderDetail) BeforeSave() error {
	return nil
}

// Prepare invoked before saving, can be used to populate fields etc.
func (p *PayOrderDetail) Prepare() {
}

// Validate invoked before performing action, return an error if field is not populated.
func (p *PayOrderDetail) Validate(action Action) error {
	return nil
}

// TableInfo return table meta data
func (p *PayOrderDetail) TableInfo() *TableInfo {
	return pay_order_detailTableInfo
}
