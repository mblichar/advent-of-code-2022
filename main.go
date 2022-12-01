package main

import (
	"fmt"
	"github.com/mblichar/advent-of-code-2022/day1"
	"github.com/mblichar/advent-of-code-2022/day2"
	"github.com/mblichar/advent-of-code-2022/day3"
	"github.com/mblichar/advent-of-code-2022/day4"
	"os"
)

func main() {
	day := os.Args[1]
	switch day {
	case "1":
		day1.Day1()
	case "2":
		day2.Day2()
	case "3":
		day3.Day3(os.Args[2])
	case "4":
		day4.Day4()
	default:
		fmt.Printf("invalid day %s", day)
	}
}
