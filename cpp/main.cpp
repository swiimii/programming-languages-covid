#include <iostream>
#include <fstream>
//#include <cpprestsdk/http_client.h>
//#include <cpprestsdk/filestream.h>
//#include <cpprestsdk/json.h>
#include <map>
#include <string>

using namespace std;
//using namespace utility;
//using namespace web;
//using namespace web::http;
//using namespace web::http::client;
//using namespace cuncurrency::streams;
//using namespace web::json;

class Stats {
public:
	map<int, bool> results;
	map<string, int> data;

	Stats(map<int, bool> dict) {
		results = dict;
		//data = &dataMap;
	}

	void AddData() {
		RetrieveData();
		string key;
		int value, questionNum;
		//Update data in map
		for (auto elem : data)
		{
			key = elem.first;
			value = elem.second;
			if (key.find("Correct") != -1) {
				questionNum = stoi(key.substr(7));
				if (results[questionNum]) {
					data[key] = value + 1;
				}
			}
			else if (key.find("Incorrect") != -1) {
				questionNum = stoi(key.substr(9));
				if (!results[questionNum]) {
					data[key] = value + 1;
				}
			}
		}
	}

	void CreateStatsDB() {
		fstream statsFile;
		statsFile.open("statsfile.txt", ios::out);
		// Add correct and incorrect counts for each question
		for (int i = 1; i <= results.size(); i++) {
			statsFile << to_string(i) << ": Correct- 0 Incorrect- 0\n";
		}
		statsFile.close();
	}

	void RetrieveData() {
		fstream statsFile("statsfile.txt");
		data.clear();
		//Go through each line in stats file and store data in map
		string l, str1, str2;
		int numQuestion, numCorrect, numIncorrect, pos1, pos2;
		while (getline(statsFile, l)) {
			pos2 = l.find(":");
			numQuestion = stoi(l.substr(0, pos2));
			pos1 = l.find("Correct") + 9;
			pos2 = l.find("Incorrect") - 1;
			numCorrect = stoi(l.substr(pos1, pos2));
			pos1 = l.find("Incorrect") + 11;
			numIncorrect = stoi(l.substr(pos1));

			str1 = "Correct" + to_string(numQuestion);
			str2 = "Incorrect" + to_string(numQuestion);
			data.insert(pair<string, int>(str1, numCorrect));
			data.insert(pair<string, int>(str2, numIncorrect));
		}
		statsFile.close();
	}

	void UpdateStats() {
		fstream statsFile;
		statsFile.open("statsfile.txt", ios::out);
		// Add correct and incorrect counts for each question
		for (int i = 1; i <= results.size(); i++) {
			statsFile << to_string(i) << ": ";
			statsFile << "Correct- " << data["Correct" + to_string(i)];
			statsFile << " Incorrect- " << data["Incorrect" + to_string(i)] << "\n";
		}
		statsFile.close();
	}
private:

};

int main()
{
	map<int, bool> exResults;
	exResults[1] = true;
	exResults[2] = false;
	exResults[3] = true;

	Stats example(exResults);
	example.CreateStatsDB();
	example.AddData();
	example.UpdateStats();


	/*for (auto elem : example.data)
	{
		cout << elem.first << ": " << elem.second << endl;
	}*/


	/*
	// HTTP request and saving results tutorial

	auto fileStream = std::make_shared<ostream>();

	// Open stream to output file.
	pplx::task<void> requestTask = fstream::open_ostream(U("results.html")).then([=](ostream outFile)
		{
			*fileStream = outFile;

			// Create http_client to send the request.
			http_client client(U("http://www.bing.com/"));

			// Build request URI and start the request.
			uri_builder builder(U("/search"));
			builder.append_query(U("q"), U("cpprestsdk github"));
			return client.request(methods::GET, builder.to_string());
		});

	// Handle response headers arriving.
	.then([=](http_response response)
		{
			printf("Received response status code:%u\n", response.status_code());

			// Write response body into the file.
			return response.body().read_to_end(fileStream->streambuf());
		});

	// Close the file stream.
	.then([=](size_t)
		{
			return fileStream->close();
		});

	// Wait for all the outstanding I/O to complete and handle any exceptions
	try
	{
		requestTask.wait();
	}
	catch (const std::exception & e)
	{
		printf("Error exception:%s\n", e.what());
	}
	*/
	return 0;
}
