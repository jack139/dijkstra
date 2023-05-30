package dijkstra

import (
	"testing"
)

func TestEmptyGraph(t *testing.T) {
	g := make(Graph)

	_, _, err := g.Path("a", "z")
	if err == nil {
		t.Error("Error nil; want error message")
	}
}

func TestGraphErrors(t *testing.T) {
	g := Graph{
		"a": {"b": {note:"note", cost:20}, "c": {note:"note", cost:80}},
		"b": {"a": {note:"note", cost:20}, "c": {note:"note", cost:20}},
		"c": {"a": {note:"note", cost:80}, "b": {note:"note", cost:20}},
	}

	_, _, err := g.Path("a", "z")
	if err == nil {
		t.Error("err = nil; want not in graph error")
	}

	_, _, err = g.Path("z", "c")
	if err == nil {
		t.Error("err = nil; want not in graph error")
	}
}

func TestPath1(t *testing.T) {
	g := Graph{
		"a": {"b": {note:"note", cost:20}, "c": {note:"note", cost:80}},
		"b": {"a": {note:"note", cost:20}, "c": {note:"note", cost:20}},
		"c": {"a": {note:"note", cost:80}, "b": {note:"note", cost:20}},
	}

	// The shortest path is correct
	path, cost, err := g.Path("a", "c")
	if err != nil {
		t.Errorf("err = %v; want nil", err)
	}

	expectedPath := []string{"a", "b", "c"}

	if len(path) != len(expectedPath) {
		t.Errorf("path = %v; want %v", path, expectedPath)
	}
	for i, key := range path {
		if key != expectedPath[i] {
			t.Errorf("path = %v; want %v", path, expectedPath)
		}
	}

	expectedCost := 40
	if cost != expectedCost {
		t.Errorf("cost = %v; want %v", cost, expectedCost)
	}
}

func TestPath2(t *testing.T) {
	g := Graph{
		"a": {"b": {note:"note", cost:7},  "c": {note:"note", cost:9}, "f": {note:"note", cost:14}},
		"b": {"c": {note:"note", cost:10}, "d": {note:"note", cost:15}},
		"c": {"d": {note:"note", cost:11}, "f": {note:"note", cost:2}},
		"d": {"e": {note:"note", cost:6}},
		"e": {"f": {note:"note", cost:9}},
	}

	// The shortest path is correct
	path, _, err := g.Path("a", "e")
	if err != nil {
		t.Errorf("err = %v; want nil", err)
	}

	expectedPath := []string{"a", "c", "d", "e"}

	if len(path) != len(expectedPath) {
		t.Errorf("path = %v; want %v", path, expectedPath)
	}
	for i, key := range path {
		if key != expectedPath[i] {
			t.Errorf("path = %v; want %v", path, expectedPath)
		}
	}
}

func BenchmarkPath(b *testing.B) {
	g := Graph{
		"a": {"b": {note:"note", cost:20}, "c": {note:"note", cost:80}},
		"b": {"a": {note:"note", cost:20}, "c": {note:"note", cost:20}},
		"c": {"a": {note:"note", cost:80}, "b": {note:"note", cost:20}},
	}

	b.ResetTimer()

	for i := 0; i < b.N; i++ {
		g.Path("a", "c")
	}
}

func TestExampleGraph_Path(t *testing.T) {
	g := Graph{
		"a": {"b": {note:"note", cost:20}, "c": {note:"note", cost:80}},
		"b": {"a": {note:"note", cost:20}, "c": {note:"note", cost:20}},
		"c": {"a": {note:"note", cost:80}, "b": {note:"note", cost:20}},
	}

	path, cost, _ := g.Path("a", "c") // skipping error handling

	t.Logf("path: %v, cost: %v", path, cost)
	// Output: path: [a b c], cost: 40
}
