package day1

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func Day1() {
	topThree := []int{0, 0, 0}
	sum := 0
	scanner := bufio.NewScanner(os.Stdin)

	updateTopThree := func() {
		insertIndex := -1
		for i := 0; i < 3; i++ {
			if sum > topThree[i] {
				insertIndex = i
				break
			}
		}

		if insertIndex != -1 {
			// shift
			for i := 2; i >= 0; i-- {
				if i > insertIndex {
					topThree[i] = topThree[i-1]
				}
			}
			topThree[insertIndex] = sum
		}
	}

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			updateTopThree()
			sum = 0
		} else {
			calories, err := strconv.Atoi(line)
			if err != nil {
				fmt.Printf("invalid line: %s %s", line, err)
				return
			}
			sum += calories
		}
	}

	// to cover last line
	updateTopThree()

	fmt.Printf("part 1: %d\n", topThree[0])
	fmt.Printf("part 2: %d\n", topThree[0]+topThree[1]+topThree[2])
}
