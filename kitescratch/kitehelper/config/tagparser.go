package config

import (
	"fmt"
	"reflect"
	"strings"
)

type simpleYamlParser struct {
	indent        int
	originalValue any
	currVal       any
}

func (p *simpleYamlParser) parse(v any) string {
	p.originalValue = v

	var sb strings.Builder

	for _, v := range reflect.VisibleFields(reflect.TypeOf(v)) {
		sb.WriteString(p.vToYaml(v))
	}

	return strings.TrimSpace(sb.String())
}

func (c *simpleYamlParser) _getValue(field string) reflect.Value {
	// Gets the value of a field in the original value or currValue using reflect
	defer func() {
		recover()
	}()

	if c.currVal != nil {
		return reflect.ValueOf(c.currVal).FieldByName(field)
	}
	return reflect.ValueOf(c.originalValue).FieldByName(field)
}

func (c *simpleYamlParser) vToYaml(v reflect.StructField) string {
	str := ""

	if v.Type == nil {
		panic("nil type")
	}

	if v.Type.Kind() == reflect.Ptr {
		panic("pointer type not supported")
	}

	switch v.Type.Kind() {
	case reflect.Struct:
		structName := v.Tag.Get("yaml")
		str += strings.Repeat(" ", c.indent*2) + structName + ":\n"
		c.indent++
		// For every field in the struct, call vToYaml
		for i := 0; i < v.Type.NumField(); i++ {
			str += c.vToYaml(v.Type.Field(i))
		}
		c.indent--

		if c.indent == 0 {
			str += "\n" // Add a newline after each struct/map
		}
	case reflect.Map:
		// Maps are similar to structs, first part is the same
		mapName := v.Tag.Get("yaml")
		str += strings.Repeat(" ", c.indent*2) + mapName + ":\n"

		// Get the map value
		mapValue := c._getValue(v.Name).Interface()

		// Get the map keys
		mapKeys := reflect.ValueOf(mapValue).MapKeys()

		// For every key, get the value and add it to the string
		for _, key := range mapKeys {
			c.indent++
			str += strings.Repeat(" ", c.indent*2) + key.String() + ":\n"
			c.indent++

			// Get the struct value
			structValue := reflect.ValueOf(reflect.ValueOf(mapValue).MapIndex(key).Interface())

			c.currVal = structValue.Interface()

			for j := 0; j < structValue.NumField(); j++ {
				str += c.vToYaml(structValue.Type().Field(j))
			}

			c.currVal = nil
			c.indent--
			c.indent--
		}

		if c.indent == 0 {
			str += "\n" // Add a newline after each struct/map
		}
	case reflect.Slice:
		vName := v.Tag.Get("yaml")

		// Get the default tag
		defTag := v.Tag.Get("default")

		if defTag == "" {
			panic("default tag is empty")
		}

		// Split the default tag by commas
		defTagSplit := strings.Split(defTag, ",")

		str += strings.Repeat(" ", c.indent*2) + vName + ":\n"

		c.indent++
		for _, s := range defTagSplit {
			str += strings.Repeat(" ", c.indent*2) + "- " + strings.TrimSpace(s) + "\n"
		}
		c.indent--
	case reflect.String, reflect.Int, reflect.Bool, reflect.Uint64, reflect.Uint32, reflect.Uint16, reflect.Uint8, reflect.Uint, reflect.Int64, reflect.Int32, reflect.Int16, reflect.Int8:
		// Get the default tag
		defTag := v.Tag.Get("default")

		valInt := fmt.Sprintf("%v", c._getValue(v.Name))

		if !strings.Contains(valInt, "<invalid reflect.Value>") {
			defTag = valInt
		}

		// Get the comment tag
		commentTag := v.Tag.Get("comment")

		// Get the required tag
		requiredTag := v.Tag.Get("required")

		if requiredTag != "true" && requiredTag != "false" {
			requiredTag = "true"
		}

		yamlName := v.Tag.Get("yaml")

		if defTag != "" {
			str += strings.Repeat(" ", c.indent*2) + yamlName + ": " + defTag
		} else {
			str += strings.Repeat(" ", c.indent*2) + yamlName + ":"
		}

		if commentTag != "" {
			str += " # " + commentTag
		}

		if requiredTag == "false" {
			if commentTag != "" {
				str += " (optional)"
			} else {
				str += " # (optional)"
			}
		}

		str += "\n"
	}

	return str
}
