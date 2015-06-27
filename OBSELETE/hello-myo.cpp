// Copyright (C) 2013-2014 Thalmic Labs Inc.
// Distributed under the Myo SDK license agreement. See LICENSE.txt for details.
#define _USE_MATH_DEFINES
#include <cmath>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <algorithm>

// The only file that needs to be included to use the Myo C++ SDK is myo.hpp.
#include <myo/myo.hpp>

using namespace System;
using namespace System::IO::Ports;

// Classes that inherit from myo::DeviceListener can be used to receive events from Myo devices. DeviceListener
// provides several virtual functions for handling different kinds of events. If you do not override an event, the
// default behavior is to do nothing.
class DataCollector : public myo::DeviceListener {
	int counter = 0;
	float w, x, y, z;
	float yaw_min, yaw_max, pitch_min, pitch_max;
	float yaw_deg = 90, pitch_deg = 25;

public:
    DataCollector()
    : onArm(false), isUnlocked(false), roll_w(0), pitch_w(0), yaw_w(0), currentPose()
    {
    }

	void init_serial()
	{
		String^ answer;
		String^ portName;
		int baudRate = 9600;
		Console::WriteLine("Type in a port name and hit ENTER");
		portName = Console::ReadLine();

		SerialPort^ arduino;
		arduino = gcnew SerialPort(portName, baudRate);

		arduino->Open();
	}

	void set_param(float y_min, float y_max, float p_min, float p_max)
	{
		yaw_min = y_min;
		yaw_max = y_max;
		pitch_min = p_min;
		pitch_max = p_max;
	}
    // onUnpair() is called whenever the Myo is disconnected from Myo Connect by the user.
    void onUnpair(myo::Myo* myo, uint64_t timestamp)
    {
        // We've lost a Myo.
        // Let's clean up some leftover state.
        roll_w = 0;
        pitch_w = 0;
        yaw_w = 0;
        onArm = false;
        isUnlocked = false;
    }

	float get_yaw()
	{
		return yaw_w;
	}

	float get_pitch()
	{
		return pitch_w;
	}

    // onOrientationData() is called whenever the Myo device provides its current orientation, which is represented
    // as a unit quaternion.
    void onOrientationData(myo::Myo* myo, uint64_t timestamp, const myo::Quaternion<float>& quat)
    {
        using std::atan2;
        using std::asin;
        using std::sqrt;
        using std::max;
        using std::min;

		float roll = atan2(2.0f * (quat.w() * quat.x() + quat.y() * quat.z()),
				1.0f - 2.0f * (quat.x() * quat.x() + quat.y() * quat.y()));
		float pitch = asin(max(-1.0f, min(1.0f, 2.0f * (quat.w() * quat.y() - quat.z() * quat.x()))));
		float yaw = atan2(2.0f * (quat.w() * quat.z() + quat.x() * quat.y()),
				 1.0f - 2.0f * (quat.y() * quat.y() + quat.z() * quat.z()));
		w = quat.w();
		x = quat.x();
		y = quat.y();
		z = quat.z();


        // Convert the floating point angles in radians to a scale from 0 to 18.
        //roll_w = static_cast<int>((roll + (float)M_PI)/(M_PI * 2.0f) * 18);
        //pitch_w = static_cast<int>((pitch + (float)M_PI/2.0f)/M_PI * 18);
       // yaw_w = static_cast<int>((yaw + (float)M_PI)/(M_PI * 2.0f) * 18);
	    roll_w = static_cast<float>((roll + (float)M_PI)/(M_PI * 2.0f) * 18);
	   pitch_w = static_cast<float>((pitch + (float)M_PI/2.0f)/M_PI * 18.0f);
	   yaw_w = static_cast<float>((yaw + (float)M_PI) / (M_PI * 2.0f) * 18.0f);

    }

    // onPose() is called whenever the Myo detects that the person wearing it has changed their pose, for example,
    // making a fist, or not making a fist anymore.
    void onPose(myo::Myo* myo, uint64_t timestamp, myo::Pose pose)
    {
        currentPose = pose;

        if (pose != myo::Pose::unknown && pose != myo::Pose::rest) {
            // Tell the Myo to stay unlocked until told otherwise. We do that here so you can hold the poses without the
            // Myo becoming locked.
            myo->unlock(myo::Myo::unlockHold);

            // Notify the Myo that the pose has resulted in an action, in this case changing
            // the text on the screen. The Myo will vibrate.
            myo->notifyUserAction();
        } else {
            // Tell the Myo to stay unlocked only for a short period. This allows the Myo to stay unlocked while poses
            // are being performed, but lock after inactivity.
            myo->unlock(myo::Myo::unlockTimed);
        }
    }

    // onArmSync() is called whenever Myo has recognized a Sync Gesture after someone has put it on their
    // arm. This lets Myo know which arm it's on and which way it's facing.
    void onArmSync(myo::Myo* myo, uint64_t timestamp, myo::Arm arm, myo::XDirection xDirection, float rotation,
                   myo::WarmupState warmupState)
    {
        onArm = true;
        whichArm = arm;
    }

    // onArmUnsync() is called whenever Myo has detected that it was moved from a stable position on a person's arm after
    // it recognized the arm. Typically this happens when someone takes Myo off of their arm, but it can also happen
    // when Myo is moved around on the arm.
    void onArmUnsync(myo::Myo* myo, uint64_t timestamp)
    {
        onArm = false;
    }

    // onUnlock() is called whenever Myo has become unlocked, and will start delivering pose events.
    void onUnlock(myo::Myo* myo, uint64_t timestamp)
    {
        isUnlocked = true;
    }

    // onLock() is called whenever Myo has become locked. No pose events will be sent until the Myo is unlocked again.
    void onLock(myo::Myo* myo, uint64_t timestamp)
    {
        isUnlocked = false;
    }

    // There are other virtual functions in DeviceListener that we could override here, like onAccelerometerData().
    // 
	
    // We define this function to print the current values that were updated by the on...() functions above.
    void print()
    {
        // Clear the current line
        std::cout << '\r';

		std::cout << '[' << std::fixed << std::setprecision(4) << roll_w << ']'
			<< '[' << std::fixed << std::setprecision(4) << pitch_w << ']'
			<< '[' << std::fixed << std::setprecision(4) << yaw_w << ']';

        if (onArm) {
            // Print out the lock state, the currently recognized pose, and which arm Myo is being worn on.

            // Pose::toString() provides the human-readable name of a pose. We can also output a Pose directly to an
            // output stream (e.g. std::cout << currentPose;). In this case we want to get the pose name's length so
            // that we can fill the rest of the field with spaces below, so we obtain it as a string using toString().
            std::string poseString = currentPose.toString();

            std::cout << '[' << (isUnlocked ? "unlocked" : "locked  ") << ']'
                      << '[' << (whichArm == myo::armLeft ? "L" : "R") << ']'
                      << '[' << poseString << std::string(14 - poseString.size(), ' ') << ']';
        } else {
            // Print out a placeholder for the arm and pose when Myo doesn't currently know which arm it's on.
            std::cout << '[' << std::string(8, ' ') << ']' << "[?]" << '[' << std::string(14, ' ') << ']';
        }

        std::cout << std::flush;
    }
	void send_serial()
	{
		float right = yaw_min;
		float left = yaw_max;
		float top = pitch_max;
		float bot = pitch_min;

		float cur_y = yaw_w;
		float cur_p = pitch_w;

		float deg_y;
		float deg_p;
		float dif;
		float range;

		bool r_is_max = false;
		if (right >= left) r_is_max = true;

		if (r_is_max) {
			range = right - left;
			dif = cur_y - left;
			deg_y = yaw_deg - dif / range * yaw_deg;

			if (cur_y < left) deg_y = yaw_deg;
			if (cur_y > right) deg_y = 0;
		}
		else {
			range = left - right;
			dif = cur_y - right;
			deg_y = dif / range * yaw_deg;

			if (cur_y > left) deg_y = yaw_deg;
			if (cur_y < right) deg_y = 0;
		}

		range = top - bot;
		dif = cur_p - bot;
		deg_p = dif / range * pitch_deg;
		if (cur_p > top) deg_p = pitch_deg;
		if (cur_p < bot) deg_p = 0;

		std::cout << deg_p << "\n";
		std::cout  << "\n";
		std::cout << deg_y << "\n";
		std::cout << "\n";

		arduino->WriteLine(""+deg_p);

		arduino->WriteLine(""+deg_y);
	}

    // These values are set by onArmSync() and onArmUnsync() above.
    bool onArm;
    myo::Arm whichArm;

    // This is set by onUnlocked() and onLocked() above.
    bool isUnlocked;

    // These values are set by onOrientationData() and onPose() above.
    float roll_w, pitch_w, yaw_w;
    myo::Pose currentPose;
};

int main(int argc, char** argv)
{
	float y_min=0, y_max=0, p_min=0, p_max=0;
    // We catch any exceptions that might occur below -- see the catch statement for more details.
    try {

    // First, we create a Hub with our application identifier. Be sure not to use the com.example namespace when
    // publishing your application. The Hub provides access to one or more Myos.
    myo::Hub hub("com.example.hello-myo");

    std::cout << "Attempting to find a Myo..." << std::endl;

    // Next, we attempt to find a Myo to use. If a Myo is already paired in Myo Connect, this will return that Myo
    // immediately.
    // waitForMyo() takes a timeout value in milliseconds. In this case we will try to find a Myo for 10 seconds, and
    // if that fails, the function will return a null pointer.
    myo::Myo* myo = hub.waitForMyo(10000);

    // If waitForMyo() returned a null pointer, we failed to find a Myo, so exit with an error message.
    if (!myo) {
        throw std::runtime_error("Unable to find a Myo!");
    }

    // We've found a Myo.
    std::cout << "Connected to a Myo armband!" << std::endl << std::endl;

    // Next we construct an instance of our DeviceListener, so that we can register it with the Hub.
    DataCollector collector;
	collector.init_serial();

    // Hub::addListener() takes the address of any object whose class inherits from DeviceListener, and will cause
    // Hub::run() to send events to all registered device listeners.
    hub.addListener(&collector);

	while (1) {
		hub.run(1000 / 20);
		std::cout << "Put your arm in the rightmost position and press 'ENTER'" << "\r";
		if (std::cin.get() == '\n')
		{
			y_min = collector.get_yaw();
			break;
		}
	}

	while (1) {
		hub.run(1000 / 20);
		std::cout << "Put your arm in the leftmost position and press 'ENTER'" << "\r";
		if (std::cin.get() == '\n')
		{
			y_max = collector.get_yaw();
			break;
		}
	}

	while (1) {
		hub.run(1000 / 20);
		std::cout << "Put your arm in the topmost position and press 'ENTER'" << "\r";
		if (std::cin.get() == '\n')
		{
			p_max = collector.get_pitch();
			break;
		}
	}

	while (1) {
		hub.run(1000 / 20);
		std::cout << "Put your arm in the bottommost position and press 'ENTER'" << "\r";
		if (std::cin.get() == '\n')
		{
			p_min = collector.get_pitch();
			break;
		}
	}

	collector.set_param(y_min, y_max, p_min, p_max);

	std::cout << '[' << std::fixed << std::setprecision(4) << y_min << ']'
		<< '[' << std::fixed << std::setprecision(4) << y_max << ']'
		<< '[' << std::fixed << std::setprecision(4) << p_max << ']'
		<< '[' << std::fixed << std::setprecision(4) << p_min << ']';

    // Finally we enter our main loop.
    while (1) {
        // In each iteration of our main loop, we run the Myo event loop for a set number of milliseconds.
        // In this case, we wish to update our display 20 times a second, so we run for 1000/20 milliseconds.
        hub.run(1000/20);
		collector.send_serial();
        // After processing events, we call the print() member function we defined above to print out the values we've
        // obtained from any events that have occurred.
        //collector.print();
    }

    // If a standard exception occurred, we print out its message and exit.
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        std::cerr << "Press enter to continue.";
        std::cin.ignore();
        return 1;
    }
}
