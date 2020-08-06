#include <iostream>
#include <fstream>
#include <map>
#include <string>

using namespace std;

class Stats {
public:
	map<int, bool> results;
	map<string, int> data;
	map<string, int> calculatedData;

	Stats(map<int, bool> dict) {
		results = dict;
	}

	void AddData() {
		RetrieveData();
		string key;
		int value, questionNum;
		//Update data in map
		for (auto elem : data) {
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
		UpdateStats();
		RetrieveData();
	}

	void CalculateStats() {
		// Calculate percentages
		double doubleVal;
		int calcVal;
		for (int i = 1; i <= 3; i++) {
			doubleVal = static_cast<double>(data["Correct" + to_string(i)]) / data["Total" + to_string(i)];
			calcVal = static_cast<int>(doubleVal * 100);
			calculatedData["%Correct" + to_string(i)] = calcVal;

			doubleVal = static_cast<double>(data["Incorrect" + to_string(i)]) / data["Total" + to_string(i)];
			calcVal = static_cast<int>(doubleVal * 100);
			calculatedData["%Incorrect" + to_string(i)] = calcVal;
		}
	}

	void CreateStatsDB() {
		fstream dataFile;
		dataFile.open("datafile.txt", ios::out);
		// Add correct and incorrect counts for each question
		for (int i = 1; i <= results.size(); i++) {
			dataFile << to_string(i) << ": Correct- 0 Incorrect- 0\n";
		}
		dataFile.close();
	}

	void RetrieveData() {
		fstream dataFile("datafile.txt");
		data.clear();
		//Go through each line in stats file and store data in map
		string l, str1, str2, str3;
		int numQuestion, numCorrect, numIncorrect, pos1, pos2;
		while (getline(dataFile, l)) {
			pos2 = l.find(":");
			numQuestion = stoi(l.substr(0, pos2));
			pos1 = l.find("Correct") + 9;
			pos2 = l.find("Incorrect") - 1;
			numCorrect = stoi(l.substr(pos1, pos2));
			pos1 = l.find("Incorrect") + 11;
			numIncorrect = stoi(l.substr(pos1));

			str1 = "Correct" + to_string(numQuestion);
			str2 = "Incorrect" + to_string(numQuestion);
			str3 = "Total" + to_string(numQuestion);
			data.insert(pair<string, int>(str1, numCorrect));
			data.insert(pair<string, int>(str2, numIncorrect));
			data.insert(pair<string, int>(str3, numIncorrect + numCorrect));
		}
		dataFile.close();
	}

	void SendData() {
		CalculateStats();
		fstream statsFile;
		statsFile.open("statsfile.txt", ios::out);
		// Add correct and incorrect counts for each question
		for (int i = 1; i <= results.size(); i++) {
			statsFile << "Question " << to_string(i) << ": ";
			if (results[i]) {
				statsFile << "Correct\n";
			}
			else {
				statsFile << "Incorrect\n";
			}
			statsFile << "Out of the " << data["Total" + to_string(i)] << " people who answered this question, ";
			statsFile << calculatedData["%Correct" + to_string(i)] << "% answered this question correctly and ";
			statsFile << calculatedData["%Incorrect" + to_string(i)] << "% answered this question incorrectly.\n";
		}
		statsFile.close();
	}

	void UpdateStats() {
		fstream dataFile;
		dataFile.open("datafile.txt", ios::out);
		// Add correct and incorrect counts for each question
		for (int i = 1; i <= results.size(); i++) {
			dataFile << to_string(i) << ": ";
			dataFile << "Correct- " << data["Correct" + to_string(i)];
			dataFile << " Incorrect- " << data["Incorrect" + to_string(i)] << "\n";
		}
		dataFile.close();
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
	example.AddData();
	example.SendData();

	return 0;
}
