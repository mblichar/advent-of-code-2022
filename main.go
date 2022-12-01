package main

import (
	"fmt"
	"github.com/mblichar/advent-of-code-2022/day1"
	"os"
)

func main() {
	day := os.Args[1]
	switch day {
	case "1":
		day1.Day1()
	default:
		fmt.Printf("invalid day %s", day)
	}
}
