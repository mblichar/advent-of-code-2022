package day4

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func Day4() {
	scanner := bufio.NewScanner(os.Stdin)

	fullyOverlapCount := 0
	overlapAtAllCount := 0
	for scanner.Scan() {
		line := scanner.Text()
		pairs := strings.Split(line, ",")
		firstPair := readPair(pairs[0])
		secondPair := readPair(pairs[1])

		if areFullyOverlapping(firstPair, secondPair) {
			fullyOverlapCount++
		}

		if areOverlappingAtAll(firstPair, secondPair) {
			overlapAtAllCount++
		}
	}

	fmt.Printf("part 1: %d\n", fullyOverlapCount)
	fmt.Printf("part 2: %d\n", overlapAtAllCount)
}

func readPair(input string) []int {
	var result []int
	for _, s := range strings.Split(input, "-") {
		i, _ := strconv.Atoi(s)
		result = append(result, i)
	}

	return result
}

func areFullyOverlapping(firstPair []int, secondPair []int) bool {
	if firstPair[0] == secondPair[0] || firstPair[1] == secondPair[1] {
		return true
	}

	if firstPair[0] > secondPair[0] {
		return firstPair[1] <= secondPair[1]
	}

	// firstPair[0] < secondPair[0]
	return firstPair[1] >= secondPair[1]
}

func areOverlappingAtAll(firstPair []int, secondPair []int) bool {
	if firstPair[1] < secondPair[0] || secondPair[1] < firstPair[0] || firstPair[0] > secondPair[1] || secondPair[0] > firstPair[1] {
		return false
	}

	return true
}
