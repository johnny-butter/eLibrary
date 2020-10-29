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


CREATE TABLE `api_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `first_name` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `api_user_email_9ef5afa6_uniq` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci

JSON Sample
-------------------------------------
{    "username": "HvyWZytYUVRtMtRiygqtWJTlQ",    "first_name": "MiITLZdrrDfErvIMZRfReONny",    "is_staff": 75,    "date_joined": "2033-02-18T00:57:15.32083773+08:00",    "is_superuser": 28,    "password": "IjFalPvWCerYMIvhXuXVvxQvp",    "last_login": "2126-08-08T09:03:14.999823697+08:00",    "last_name": "QnBEuSlLUEfarrbmpbocKATgi",    "email": "jSBSgAbiTfmyChUpvSQgNYRhf",    "is_active": 6,    "id": 28}



*/

// APIUser struct is a row record of the api_user table in the dk0fw2stwwcn00cc database
type APIUser struct {
	//[ 0] id                                             int                  null: false  primary: true   isArray: false  auto: true   col: int             len: -1      default: []
	ID int32 `gorm:"primary_key;AUTO_INCREMENT;column:id;type:int;"`
	//[ 1] password                                       varchar(128)         null: false  primary: false  isArray: false  auto: false  col: varchar         len: 128     default: []
	Password string `gorm:"column:password;type:varchar;size:128;"`
	//[ 2] last_login                                     datetime             null: true   primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	LastLogin null.Time `gorm:"column:last_login;type:datetime;"`
	//[ 3] is_superuser                                   tinyint              null: false  primary: false  isArray: false  auto: false  col: tinyint         len: -1      default: []
	IsSuperuser int32 `gorm:"column:is_superuser;type:tinyint;"`
	//[ 4] username                                       varchar(150)         null: false  primary: false  isArray: false  auto: false  col: varchar         len: 150     default: []
	Username string `gorm:"column:username;type:varchar;size:150;"`
	//[ 5] first_name                                     varchar(30)          null: false  primary: false  isArray: false  auto: false  col: varchar         len: 30      default: []
	FirstName string `gorm:"column:first_name;type:varchar;size:30;"`
	//[ 6] last_name                                      varchar(150)         null: false  primary: false  isArray: false  auto: false  col: varchar         len: 150     default: []
	LastName string `gorm:"column:last_name;type:varchar;size:150;"`
	//[ 7] email                                          varchar(254)         null: true   primary: false  isArray: false  auto: false  col: varchar         len: 254     default: []
	Email null.String `gorm:"column:email;type:varchar;size:254;"`
	//[ 8] is_staff                                       tinyint              null: false  primary: false  isArray: false  auto: false  col: tinyint         len: -1      default: []
	IsStaff int32 `gorm:"column:is_staff;type:tinyint;"`
	//[ 9] is_active                                      tinyint              null: false  primary: false  isArray: false  auto: false  col: tinyint         len: -1      default: []
	IsActive int32 `gorm:"column:is_active;type:tinyint;"`
	//[10] date_joined                                    datetime             null: false  primary: false  isArray: false  auto: false  col: datetime        len: -1      default: []
	DateJoined time.Time `gorm:"column:date_joined;type:datetime;"`
}

var api_userTableInfo = &TableInfo{
	Name: "api_user",
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
			Name:               "password",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(128)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       128,
			GoFieldName:        "Password",
			GoFieldType:        "string",
			JSONFieldName:      "password",
			ProtobufFieldName:  "password",
			ProtobufType:       "string",
			ProtobufPos:        2,
		},

		&ColumnInfo{
			Index:              2,
			Name:               "last_login",
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
			GoFieldName:        "LastLogin",
			GoFieldType:        "null.Time",
			JSONFieldName:      "last_login",
			ProtobufFieldName:  "last_login",
			ProtobufType:       "google.protobuf.Timestamp",
			ProtobufPos:        3,
		},

		&ColumnInfo{
			Index:              3,
			Name:               "is_superuser",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "tinyint",
			DatabaseTypePretty: "tinyint",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "tinyint",
			ColumnLength:       -1,
			GoFieldName:        "IsSuperuser",
			GoFieldType:        "int32",
			JSONFieldName:      "is_superuser",
			ProtobufFieldName:  "is_superuser",
			ProtobufType:       "int32",
			ProtobufPos:        4,
		},

		&ColumnInfo{
			Index:              4,
			Name:               "username",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(150)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       150,
			GoFieldName:        "Username",
			GoFieldType:        "string",
			JSONFieldName:      "username",
			ProtobufFieldName:  "username",
			ProtobufType:       "string",
			ProtobufPos:        5,
		},

		&ColumnInfo{
			Index:              5,
			Name:               "first_name",
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
			GoFieldName:        "FirstName",
			GoFieldType:        "string",
			JSONFieldName:      "first_name",
			ProtobufFieldName:  "first_name",
			ProtobufType:       "string",
			ProtobufPos:        6,
		},

		&ColumnInfo{
			Index:              6,
			Name:               "last_name",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(150)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       150,
			GoFieldName:        "LastName",
			GoFieldType:        "string",
			JSONFieldName:      "last_name",
			ProtobufFieldName:  "last_name",
			ProtobufType:       "string",
			ProtobufPos:        7,
		},

		&ColumnInfo{
			Index:              7,
			Name:               "email",
			Comment:            ``,
			Notes:              ``,
			Nullable:           true,
			DatabaseTypeName:   "varchar",
			DatabaseTypePretty: "varchar(254)",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "varchar",
			ColumnLength:       254,
			GoFieldName:        "Email",
			GoFieldType:        "null.String",
			JSONFieldName:      "email",
			ProtobufFieldName:  "email",
			ProtobufType:       "string",
			ProtobufPos:        8,
		},

		&ColumnInfo{
			Index:              8,
			Name:               "is_staff",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "tinyint",
			DatabaseTypePretty: "tinyint",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "tinyint",
			ColumnLength:       -1,
			GoFieldName:        "IsStaff",
			GoFieldType:        "int32",
			JSONFieldName:      "is_staff",
			ProtobufFieldName:  "is_staff",
			ProtobufType:       "int32",
			ProtobufPos:        9,
		},

		&ColumnInfo{
			Index:              9,
			Name:               "is_active",
			Comment:            ``,
			Notes:              ``,
			Nullable:           false,
			DatabaseTypeName:   "tinyint",
			DatabaseTypePretty: "tinyint",
			IsPrimaryKey:       false,
			IsAutoIncrement:    false,
			IsArray:            false,
			ColumnType:         "tinyint",
			ColumnLength:       -1,
			GoFieldName:        "IsActive",
			GoFieldType:        "int32",
			JSONFieldName:      "is_active",
			ProtobufFieldName:  "is_active",
			ProtobufType:       "int32",
			ProtobufPos:        10,
		},

		&ColumnInfo{
			Index:              10,
			Name:               "date_joined",
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
			GoFieldName:        "DateJoined",
			GoFieldType:        "time.Time",
			JSONFieldName:      "date_joined",
			ProtobufFieldName:  "date_joined",
			ProtobufType:       "google.protobuf.Timestamp",
			ProtobufPos:        11,
		},
	},
}

// TableName sets the insert table name for this struct type
func (a *APIUser) TableName() string {
	return "api_user"
}

// BeforeSave invoked before saving, return an error if field is not populated.
func (a *APIUser) BeforeSave() error {
	return nil
}

// Prepare invoked before saving, can be used to populate fields etc.
func (a *APIUser) Prepare() {
}

// Validate invoked before performing action, return an error if field is not populated.
func (a *APIUser) Validate(action Action) error {
	return nil
}

// TableInfo return table meta data
func (a *APIUser) TableInfo() *TableInfo {
	return api_userTableInfo
}
