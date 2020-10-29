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


CREATE TABLE `book` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `publish_date` datetime(6) DEFAULT NULL,
  `price_origin` int(11) NOT NULL,
  `price_discount` int(11) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `publish_company_id` int(11) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  `update_at` datetime(6) DEFAULT NULL,
  `stock` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `book_type_id_6f4733cb_fk_book_type_id` (`type_id`),
  KEY `book_author_id_c4d52965_fk_author_id` (`author_id`),
  KEY `book_publish_company_id_fea4cfb3_fk_publish_company_id` (`publish_company_id`),
  CONSTRAINT `book_author_id_c4d52965_fk_author_id` FOREIGN KEY (`author_id`) REFERENCES `author` (`id`),
  CONSTRAINT `book_publish_company_id_fea4cfb3_fk_publish_company_id` FOREIGN KEY (`publish_company_id`) REFERENCES `publish_company` (`id`),
  CONSTRAINT `book_type_id_6f4733cb_fk_book_type_id` FOREIGN KEY (`type_id`) REFERENCES `book_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

JSON Sample
-------------------------------------
{    "publish_company_id": 37,    "stock": 32,    "price_origin": 60,    "price_discount": 76,    "author_id": 54,    "type_id": 79,    "update_at": "2064-03-29T03:29:29.977190864+08:00",    "id": 32,    "name": "QnhouJujgxuEEjCrMngAAkGpI",    "publish_date": "2286-05-14T12:04:17.74532247+08:00"}



*/

// Book struct is a row record of the book table in the dk0fw2stwwcn00cc database
type Book struct {
	//[ 0] id                                             int                  null: false  primary: true   isArray: false  auto: true   col: int             len: -1      default: []
	ID int32 `gorm:"primary_key;AUTO_INCREMENT;column:id;type:int;"`
	//[ 1] name                                           varchar(30)          null: false  primary: false  isArray: false  auto: false  col: varchar         len: 30      default: []
	Name string `gorm:"column:name;type:varchar;size:30;"`
	//[ 2] publish_date                                   datetime             null: true   primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	PublishDate null.Time `gorm:"column:publish_date;type:datetime;"`
	//[ 3] price_origin                                   int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	PriceOrigin int32 `gorm:"column:price_origin;type:int;"`
	//[ 4] price_discount                                 int                  null: true   primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	PriceDiscount null.Int `gorm:"column:price_discount;type:int;"`
	//[ 5] author_id                                      int                  null: true   primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	AuthorID null.Int `gorm:"column:author_id;type:int;"`
	//[ 6] publish_company_id                             int                  null: true   primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	PublishCompanyID null.Int `gorm:"column:publish_company_id;type:int;"`
	//[ 7] type_id                                        int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	TypeID int32 `gorm:"column:type_id;type:int;"`
	//[ 8] update_at                                      datetime             null: true   primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	UpdateAt null.Time `gorm:"column:update_at;type:datetime;"`
	//[ 9] stock                                          int                  null: false  primary: false  isArray: false  auto: false  col: int             len: -1      default: []
	Stock int32 `gorm:"column:stock;type:int;"`
}

var bookTableInfo = &TableInfo{
	Name: "book",
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
			Name:               "name",
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
			GoFieldName:        "Name",
			GoFieldType:        "string",
			JSONFieldName:      "name",
			ProtobufFieldName:  "name",
			ProtobufType:       "string",
			ProtobufPos:        2,
		},

		&ColumnInfo{
			Index:              2,
			Name:               "publish_date",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "datetime",
			DatabaseTypePretty: "datetime",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "datetime",
			ColumnLength:       -1,
			GoFieldName:        "PublishDate",
			GoFieldType:        "null.Time",
			JSONFieldName:      "publish_date",
			ProtobufFieldName:  "publish_date",
			ProtobufType:       "google.protobuf.Timestamp",
			ProtobufPos:        3,
		},

		&ColumnInfo{
			Index:              3,
			Name:               "price_origin",
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
			GoFieldName:        "PriceOrigin",
			GoFieldType:        "int32",
			JSONFieldName:      "price_origin",
			ProtobufFieldName:  "price_origin",
			ProtobufType:       "int32",
			ProtobufPos:        4,
		},

		&ColumnInfo{
			Index:              4,
			Name:               "price_discount",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "int",
			DatabaseTypePretty: "int",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "int",
			ColumnLength:       -1,
			GoFieldName:        "PriceDiscount",
			GoFieldType:        "null.Int",
			JSONFieldName:      "price_discount",
			ProtobufFieldName:  "price_discount",
			ProtobufType:       "int32",
			ProtobufPos:        5,
		},

		&ColumnInfo{
			Index:              5,
			Name:               "author_id",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "int",
			DatabaseTypePretty: "int",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "int",
			ColumnLength:       -1,
			GoFieldName:        "AuthorID",
			GoFieldType:        "null.Int",
			JSONFieldName:      "author_id",
			ProtobufFieldName:  "author_id",
			ProtobufType:       "int32",
			ProtobufPos:        6,
		},

		&ColumnInfo{
			Index:              6,
			Name:               "publish_company_id",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "int",
			DatabaseTypePretty: "int",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "int",
			ColumnLength:       -1,
			GoFieldName:        "PublishCompanyID",
			GoFieldType:        "null.Int",
			JSONFieldName:      "publish_company_id",
			ProtobufFieldName:  "publish_company_id",
			ProtobufType:       "int32",
			ProtobufPos:        7,
		},

		&ColumnInfo{
			Index:              7,
			Name:               "type_id",
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
			GoFieldName:        "TypeID",
			GoFieldType:        "int32",
			JSONFieldName:      "type_id",
			ProtobufFieldName:  "type_id",
			ProtobufType:       "int32",
			ProtobufPos:        8,
		},

		&ColumnInfo{
			Index:              8,
			Name:               "update_at",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "datetime",
			DatabaseTypePretty: "datetime",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "datetime",
			ColumnLength:       -1,
			GoFieldName:        "UpdateAt",
			GoFieldType:        "null.Time",
			JSONFieldName:      "update_at",
			ProtobufFieldName:  "update_at",
			ProtobufType:       "google.protobuf.Timestamp",
			ProtobufPos:        9,
		},

		&ColumnInfo{
			Index:              9,
			Name:               "stock",
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
			GoFieldName:        "Stock",
			GoFieldType:        "int32",
			JSONFieldName:      "stock",
			ProtobufFieldName:  "stock",
			ProtobufType:       "int32",
			ProtobufPos:        10,
		},
	},
}

// TableName sets the insert table name for this struct type
func (b *Book) TableName() string {
	return "book"
}

// BeforeSave invoked before saving, return an error if field is not populated.
func (b *Book) BeforeSave() error {
	return nil
}

// Prepare invoked before saving, can be used to populate fields etc.
func (b *Book) Prepare() {
}

// Validate invoked before performing action, return an error if field is not populated.
func (b *Book) Validate(action Action) error {
	return nil
}

// TableInfo return table meta data
func (b *Book) TableInfo() *TableInfo {
	return bookTableInfo
}
