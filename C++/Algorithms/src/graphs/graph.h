#ifndef GRAPH_H
#define GRAPH_H

#include<unordered_map>
#include<vector>
#include<set>
#include<map>
#include<deque>

#include<fstream>

namespace graph
{

	using namespace std;
	using GraphBody = unordered_map<int, set<int>>;

	class Graph
	{
	public:
		Graph(bool is_oriented);

		void Add(int start, int end);
		bool Find(int start, int end);
		size_t GetVertexNumb() const;

		// Algorithms based on DFS
		void DFS();
		map<size_t, vector<int>> ConnectedCompNumb();
		map<size_t, vector<int>> StrongConnectedCompNumb();

		bool IsCircleDetect();

		void TopoligicalSort();
		vector<int> TopologicalSortDFS();

		// Algorithms based on BFS
		void BFS(size_t start_id);
		vector<size_t> ShortestDistance(size_t start_id, size_t end_id);

		friend ostream & operator<<(ostream & os, const Graph & gr);

	private:
		void AddHelper(int start, int end);

		void Explore(unordered_map<int, bool> & is_visited, int vertex_id);

		void Explore(unordered_map<int, bool> & is_visited, int vertex_id, 
					 unordered_map<int, size_t> & cc_numb, size_t cur_cc_id);

		void ExploreHelper(unordered_map<int, bool> & is_visited, int vertex_id,
					 unordered_map<int, pair<size_t, size_t>> & times, size_t & cur_time, 
					 bool & is_circle);

		void ExploreHelperTopSort(unordered_map<int, bool> & is_visited, int vertex_id, vector<int> & top_sort_out);

	private:
		bool is_oriented_;
		size_t vertex_count_;

		GraphBody body_;
	};


	struct WeightNode
	{
		size_t end_id;
		int w;

		WeightNode(size_t _end_id, int weight) : end_id(_end_id), w(weight) {}

		friend bool operator<(const WeightNode & left, const WeightNode & right);
		friend bool operator==(const WeightNode & left, const WeightNode & right);

		friend ostream & operator<<(ostream & os, const WeightNode & wn);

	};


	using WeightGraphBody = unordered_map<size_t, set<WeightNode>>;

	class GraphWeight
	{
	public:
		GraphWeight() {}

		void Add(size_t start_id, size_t end_id, int weight);

		vector<size_t> ChipestPath(size_t start_id, size_t end_id);
		int ChipestPathCost(size_t start_id, size_t end_id);

		friend ostream & operator<<(ostream & os, const GraphWeight & wg);

	private:
		int GetWeight(size_t start_id, size_t end_id);

		void DijkstraHelper(size_t start_id, vector<int> & dist, vector<size_t> & prev);

	private:
		WeightGraphBody body_;
	};
	

}

#endif // !GRAPH_H