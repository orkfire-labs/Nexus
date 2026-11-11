// Go (go build) — math/big for big integers, GC-managed trees
package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
)

const mod = 1000000007

func factmod(n uint64) uint64 {
	var r uint64 = 1
	for i := uint64(1); i <= n; i++ {
		r = (r * i) % mod
	}
	return r
}

func bigfact(n int64) int64 {
	r := big.NewInt(1)
	t := new(big.Int)
	for i := int64(2); i <= n; i++ {
		t.SetInt64(i)
		r.Mul(r, t)
	}
	return int64(r.BitLen())
}

func fib(n int) int64 {
	if n < 2 {
		return int64(n)
	}
	return fib(n-1) + fib(n-2)
}

type Node struct{ l, r *Node }

func make_(d int) *Node {
	if d > 0 {
		return &Node{make_(d - 1), make_(d - 1)}
	}
	return &Node{}
}

func check(n *Node) int64 {
	if n.l == nil {
		return 1
	}
	return 1 + check(n.l) + check(n.r)
}

func trees(maxd int) int64 {
	keep := make_(maxd)
	var total int64
	for d := 4; d <= maxd; d += 2 {
		it := int64(1) << (maxd - d + 4)
		for i := int64(0); i < it; i++ {
			total += check(make_(d))
		}
	}
	return total + check(keep)
}

func sieve(n int) int64 {
	s := make([]bool, n+1)
	for i := 2; i <= n; i++ {
		s[i] = true
	}
	for i := 2; i*i <= n; i++ {
		if s[i] {
			for j := i * i; j <= n; j += i {
				s[j] = false
			}
		}
	}
	var c int64
	for _, v := range s {
		if v {
			c++
		}
	}
	return c
}

func main() {
	w := os.Args[1]
	var n int64
	if len(os.Args) > 2 {
		n, _ = strconv.ParseInt(os.Args[2], 10, 64)
	}
	var out int64
	switch w {
	case "factmod":
		out = int64(factmod(uint64(n)))
	case "bigfact":
		out = bigfact(n)
	case "fib":
		out = fib(int(n))
	case "trees":
		out = trees(int(n))
	case "sieve":
		out = sieve(int(n))
	}
	fmt.Println(out)
}
