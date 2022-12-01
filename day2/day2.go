package day2

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func Day2() {
	scanner := bufio.NewScanner(os.Stdin)

	// X, Y, Z is translated to A, B, C while reading move input
	inputToMove := map[byte]byte{
		'A': 'R',
		'B': 'P',
		'C': 'S',
	}

	inputToResult := map[byte]byte{
		'X': 'L',
		'Y': 'D',
		'Z': 'W',
	}
	moveScore := map[byte]int{
		'R': 1,
		'P': 2,
		'S': 3,
	}

	gameResultScore := map[string]int{
		"RR": 3,
		"PP": 3,
		"SS": 3,
		"RP": 6, // rock vs paper
		"RS": 0, // rock vs scissors
		"PR": 0, // paper vs rock
		"PS": 6, // paper vs scissors
		"SR": 6, // scissors vs rock
		"SP": 0, // scissors vs paper
	}

	expectedResultToScore := map[byte]int{
		'L': 0, // lose
		'D': 3, // draw
		'W': 6, // win
	}

	// Map to get the score for the expected move in part 2, each entry have the following like:
	// "LR": 'S'
	// L means that player should lose, R is opponent move and 'S' is player move
	resultAndOpponentMoveToPlayerMove := map[string]byte{
		"LR": 'S',
		"LP": 'R',
		"LS": 'P',
		"DR": 'R',
		"DP": 'P',
		"DS": 'S',
		"WR": 'P',
		"WP": 'S',
		"WS": 'R',
	}

	partOneScore := 0
	partTwoScore := 0
	for scanner.Scan() {
		line := scanner.Text()
		tokens := strings.Split(line, " ")

		opponentMove, playerMove := inputToMove[tokens[0][0]], inputToMove[tokens[1][0]-('X'-'A')]
		partOneScore += moveScore[playerMove] + gameResultScore[string([]byte{opponentMove, playerMove})]

		expectedResult := inputToResult[tokens[1][0]]
		partTwoScore += expectedResultToScore[expectedResult] +
			moveScore[resultAndOpponentMoveToPlayerMove[string([]byte{expectedResult, opponentMove})]]

	}

	fmt.Printf("part 1: %d\n", partOneScore)
	fmt.Printf("part 2: %d\n", partTwoScore)
}
