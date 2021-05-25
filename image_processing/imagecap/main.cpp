#include <opencv2/opencv.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <ctime>

using namespace std;
using namespace cv;

int main(int argc, char** argv){
	int CAM_ID = -1;
	char buf[256];
	Mat frame1;
	int ret;

	time_t curr_time;
	struct tm* curr_tm;

	VideoCapture cap(CAM_ID);
	if(!cap.isOpened()){
		printf("Can't open the CAM(%d)\n", CAM_ID);
		return -1;
	}
	while(1){
		cap >> frame1;
		imshow("CAM_Window", frame1);
		ret = waitKey(10);
		if(ret >= 0){
			if(ret == 99 || ret == 67){
				curr_time = time(NULL);
				curr_tm = localtime(&curr_time);
				sprintf(buf, "img_%02d%02d%02d.jpg", curr_tm->tm_hour, curr_tm->tm_min, curr_tm->tm_sec);
				cout << buf << endl;
				imwrite(buf, frame1);
			}
			else break;
		}
	}
	destroyWindow("CAM_Window");
	return 0;
}
