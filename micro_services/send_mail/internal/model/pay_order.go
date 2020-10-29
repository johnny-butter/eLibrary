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


CREATE TABLE `pay_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `state` int(11) NOT NULL,
  `total_price` decimal(10,3) NOT NULL,
  `pay_type` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `create_date` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pay_order_user_id_4522f8ab_fk_api_user_id` (`user_id`),
  CONSTRAINT `pay_order_user_id_4522f8ab_fk_api_user_id` FOREIGN KEY (`user_id`) REFERENCES `api_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

JSON Sample
-------------------------------------
{    "id": 95,    "state": 39,    "total_price": 0.4401241618992477,    "pay_type": "PthKxRwIZgDOwIuxBisyJdpqV",    "create_date": "2236-11-02T22:04:43.451845272+08:00",    "user_id": 51}



*/

// PayOrder struct is a row record of the pay_order table in the dk0fw2stwwcn00cc database
type PayOrder struct {
	//[ 0] id                                             int                  null: false  primary: true   isArray: false  auto: true   col: int             len: -1      default: []
	ID int32 `gorm:"primary_key;AUTO_INCREMENT;column:id;type:int;"`
	//[ 1] state                                          int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	State int32 `gorm:"column:state;type:int;"`
	//[ 2] total_price                                    decimal              null: false  primary: false  isArray: false  auto: false  col: decimal         len: -1      default: []
	TotalPrice float64 `gorm:"column:total_price;type:decimal;"`
	//[ 3] pay_type                                       varchar(30)          null: false  primary: false  isArray: false  auto: false  col: varchar         len: 30      default: []
	PayType string `gorm:"column:pay_type;type:varchar;size:30;"`
	//[ 4] create_date                                    datetime             null: false  primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	CreateDate time.Time `gorm:"column:create_date;type:datetime;"`
	//[ 5] user_id                                        int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	UserID int32 `gorm:"column:user_id;type:int;"`

	User APIUser
}

var pay_orderTableInfo = &TableInfo{
	Name: "pay_order",
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
			Name:               "state",
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
			GoFieldName:        "State",
			GoFieldType:        "int32",
			JSONFieldName:      "state",
			ProtobufFieldName:  "state",
			ProtobufType:       "int32",
			ProtobufPos:        2,
		},

		&ColumnInfo{
			Index:              2,
			Name:               "total_price",
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
			GoFieldName:        "TotalPrice",
			GoFieldType:        "float64",
			JSONFieldName:      "total_price",
			ProtobufFieldName:  "total_price",
			ProtobufType:       "float",
			ProtobufPos:        3,
		},

		&ColumnInfo{
			Index:              3,
			Name:               "pay_type",
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
			GoFieldName:        "PayType",
			GoFieldType:        "string",
			JSONFieldName:      "pay_type",
			ProtobufFieldName:  "pay_type",
			ProtobufType:       "string",
			ProtobufPos:        4,
		},

		&ColumnInfo{
			Index:              4,
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
			ProtobufPos:        5,
		},

		&ColumnInfo{
			Index:              5,
			Name:               "user_id",
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
			GoFieldName:        "UserID",
			GoFieldType:        "int32",
			JSONFieldName:      "user_id",
			ProtobufFieldName:  "user_id",
			ProtobufType:       "int32",
			ProtobufPos:        6,
		},
	},
}

// TableName sets the insert table name for this struct type
func (p *PayOrder) TableName() string {
	return "pay_order"
}

// BeforeSave invoked before saving, return an error if field is not populated.
func (p *PayOrder) BeforeSave() error {
	return nil
}

// Prepare invoked before saving, can be used to populate fields etc.
func (p *PayOrder) Prepare() {
}

// Validate invoked before performing action, return an error if field is not populated.
func (p *PayOrder) Validate(action Action) error {
	return nil
}

// TableInfo return table meta data
func (p *PayOrder) TableInfo() *TableInfo {
	return pay_orderTableInfo
}
