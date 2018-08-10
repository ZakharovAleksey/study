#include"unit_test\unit_test.h"
#include"sorting\sorting.h"
#include"data_structures\data_structures.h"
#include"data_structures\bloom_filter.h"
#include"practice\practice.h"

#include"data_structures\splay_tree.h"
#include"data_structures\bin_search_tree.h"
#include"data_structures\prefix_tree.h"
#include"data_structures\b_tree.h"
#include"data_structures\rb_tree.h"

#include"data_structures/heaps.h"
#include"data_structures\cartesian_tree.h"

// Graph
#include"graphs\graph.h"

#include<iostream>
#include<vector>
#include<tuple>
#include<iterator>

using namespace std;
using namespace unit_test;
using namespace sort;
using namespace bloom_filter;
using namespace practice;

void TestAll();


int main() 
{
	//TestAll();

	graph::Graph gr(true);
	gr.Add(0, 1);
	gr.Add(1, 2);
	//gr.Add(2, 4);
	gr.Add(1, 4);
	gr.Add(4, 3);
	gr.Add(3, 2);
	//gr.Add(1, 3);
	//gr.Add(1, 2);
	//gr.Add(2, 3);
	//gr.Add(3, 4);
	//gr.Add(3, 0);
	//gr.Add(3, 1);
	//gr.Add(4, 0);
	//gr.Add(4, 1);

	//gr.Add(5, 6);
	//gr.Add(6, 7);

	//gr.Add(8, 8);



	cout << gr;
	cout << "v numb = " << gr.GetVertexNumb() << endl;
	gr.DFS();

	auto res = gr.ConnsectedCompNumb();
	for (const auto & i : res)
	{
		cout << i.first << ": ";
		copy(begin(i.second), end(i.second), ostream_iterator<int>(cout, " "));
		cout << endl;
	}
	
	cout << gr.IsCircleDetect() << endl;
	
	gr.TopoligicalSort();
		

	return 0;
}

void TestAll()
{
	TestRunner tr;

	// Sorting

	tr.RunTest(sort::TestInsertionSort,			"TestInsertionSort");
	tr.RunTest(sort::TestSelectSort,			"TestSelectSort");
	tr.RunTest(sort::BubbleSortTest,			"BubbleSortTest");
	tr.RunTest(sort::HeapSortTest,				"HeapSortTest");
	tr.RunTest(sort::MergeSortTest,				"MergeSortTest");
	tr.RunTest(sort::QuickSortTest,				"QuickSortTest");
	tr.RunTest(sort::KthOrderStatisticsTest,	"KthOrderStatisticsTest");
	tr.RunTest(sort::CountingSortTest,			"CountingSort");

	// Data Structures

	tr.RunTest(data_struct::HashTableTest, "HashTableTest");
	//tr.RunTest(data_struct::BinTreeTest, "BinTreeTest");
	tr.RunTest(data_struct::DequeTest, "DequeTest");

	tr.RunTest(tree::SplayTreeTest, "SplayTreeTest");
	tr.RunTest(tree::BSTreeTest, "BSTreeTest");
	tr.RunTest(tree::TrieTreeTest, "TrieTreeTest");
	tr.RunTest(tree::BTreeTest, "BTreeTest");
	tr.RunTest(tree::RBTreeTest, "RBTreeTest");

	// Heaps
	tr.RunTest(heap::BinHeapTest, "BinHeapTest");
	tr.RunTest(heap::BinomHeapTest, "BinomHeapTest");
	tr.RunTest(tree::TestCartesianTree, "TestCartesianTree");
}