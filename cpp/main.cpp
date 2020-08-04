#include <iostream>
#include <fstream>
//#include <cpprest/http_client.h>
//#include <cpprest/filestream.h>
//#include <cpprest/json.h>
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
	map<int, int*> data;

	Stats(map<int, bool> dict) {
		results = dict;
	}

	void AddData() {
		RetrieveData();
		fstream statsFile("statsfile.txt");
		string newData;
		int questionData;
		//int questionData[2];
		//pair<int, int[2]> questionData;
		map<int, int*>::iterator iter;
		//Add results from user to stats file
		for (int i = 1; i <= data.size(); i++) {
			iter = data.find(i);
			questionData = *data[i];
			//Increment either correct or incorrect depending on user's results
			/*if (results[i]) {
				questionData[0]++;
			}
			else {
				questionData[1]++;
			}*/
			//statsFile << to_string(i) << ": Correct- " << to_string(questionData[0]) << " Incorrect- " << to_string(questionData[1]) << "\n";
			cout << questionData << endl;
		}

		//Add results from user to stats file
		string l;
		while (getline(statsFile, l)) {
			int numQuestion, numCorrect, numIncorrect;
			int pos1, pos2;

			pos2 = l.find(":");
			numQuestion = stoi(l.substr(0, pos2));
			pos1 = l.find("Correct") + 9;
			pos2 = l.find("Incorrect") - 1;
			numCorrect = stoi(l.substr(pos1, pos2));
			pos1 = l.find("Incorrect") + 11;
			numIncorrect = stoi(l.substr(pos1));

			int values[] = { numCorrect, numIncorrect };
			data[numQuestion] = values;
		}
		statsFile.close();
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
		string l;
		while (getline(statsFile, l)) {
			int numQuestion, numCorrect, numIncorrect;
			int pos1, pos2;

			pos2 = l.find(":");
			numQuestion = stoi(l.substr(0, pos2));
			pos1 = l.find("Correct") + 9;
			pos2 = l.find("Incorrect") - 1;
			numCorrect = stoi(l.substr(pos1, pos2));
			pos1 = l.find("Incorrect") + 11;
			numIncorrect = stoi(l.substr(pos1));

			cout << numQuestion << ": " << numCorrect << " " << numIncorrect << endl;
			int values[] = { numCorrect, numIncorrect };
			data[numQuestion] = values;
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
	//example.CreateStatsDB();
	example.RetrieveData();

	for (auto elem : example.data)
	{
		cout << elem.first << ": " << elem.second << " " << endl;
	}


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
