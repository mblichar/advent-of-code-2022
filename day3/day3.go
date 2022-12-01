package day3

import (
	"bufio"
	"fmt"
	"os"
)

func Day3(part string) {
	switch part {
	case "1":
		partOne()
	case "2":
		partTwo()
	}
}

func partOne() {
	scanner := bufio.NewScanner(os.Stdin)
	sum := 0
	for scanner.Scan() {
		line := scanner.Text()

		itemsSet := map[byte]bool{}
		for i := 0; i < len(line)/2; i++ {
			itemsSet[line[i]] = true
		}

		for i := len(line) / 2; i < len(line); i++ {
			if _, exists := itemsSet[line[i]]; exists {
				sum += int(priority(line[i]))
				// so it's not detected again
				delete(itemsSet, line[i])
			}
		}
	}

	fmt.Printf("part 1: %d", sum)
}

func partTwo() {
	scanner := bufio.NewScanner(os.Stdin)
	sum := 0
	groupLine := 0
	itemsInAllRucksacks := map[byte]bool{}
	for scanner.Scan() {
		line := scanner.Text()

		if groupLine == 0 {
			itemsInAllRucksacks = map[byte]bool{}
			for _, item := range line {
				itemsInAllRucksacks[byte(item)] = true
			}
		} else {
			newItemsInAllRucksacks := map[byte]bool{}
			for _, item := range line {
				if _, exists := itemsInAllRucksacks[byte(item)]; exists {
					newItemsInAllRucksacks[byte(item)] = true
				}
			}

			itemsInAllRucksacks = newItemsInAllRucksacks
		}

		if groupLine == 2 {
			if len(itemsInAllRucksacks) != 1 {
				panic(any("more than one item type shared by all rucksacks"))
			}

			// it should iterate only once
			for key := range itemsInAllRucksacks {
				sum += int(priority(key))
			}
		}

		groupLine = (groupLine + 1) % 3
	}

	fmt.Printf("part 2: %d", sum)
}

func priority(item byte) byte {
	if item >= 'a' {
		return item - 'a' + 1
	}

	return item - 'A' + 27
}
