#define Phoenix_No_WPI // remove WPI dependencies
#include "ctre/Phoenix.h"
#include "ctre/phoenix/platform/Platform.h"
#include "ctre/phoenix/unmanaged/Unmanaged.h"
#include <string>
#include <iostream>
#include <chrono>
#include <thread>
#include <SDL2/SDL.h>
#include <unistd.h>
#include <time.h>
#include <stdio.h>

using namespace ctre::phoenix;
using namespace ctre::phoenix::platform;
using namespace ctre::phoenix::motorcontrol;
using namespace ctre::phoenix::motorcontrol::can;

TalonSRX tal(0);
TalonSRX tal3(3);

void initRobot()
{
	double kTimeoutMS = 50;
	double KPIDLoopIdx = 0;
	// Configures robot
	tal.ConfigFactoryDefault();
	// set sensor
	tal.ConfigSelectedFeedbackSensor(FeedbackDevice::CTRE_MagEncoder_Relative, 0, kTimeoutMS);
	tal.SetSensorPhase(false);
	 //set peak and nominal output
	tal.ConfigNominalOutputForward(0, kTimeoutMS);
	tal.ConfigNominalOutputReverse(0, kTimeoutMS);
	tal.ConfigPeakOutputForward(1, kTimeoutMS);
	tal.ConfigPeakOutputReverse(-1, kTimeoutMS);
	
	//set closed loop gains in slot 0
	tal.Config_kF(KPIDLoopIdx, .0474, kTimeoutMS);
	tal.Config_kP(KPIDLoopIdx, 0, kTimeoutMS);
	tal.Config_kI(KPIDLoopIdx, 0, kTimeoutMS);
	tal.Config_kD(KPIDLoopIdx, 0, kTimeoutMS);

	tal.SetInverted(false);
	tal3.Follow(tal);
	tal3.SetInverted(true); //match whatever the talon is doing
} 

void sleepApp(int ms)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}


/*
void drive(double fwd, double turn)
{
	double left = fwd - turn;
	double rght = fwd + turn;  positive turn means turn robot LEFT 

	//talLeft.Set(ControlMode::PercentOutput, left);
	talRght.Set(ControlMode::PercentOutput, .2);
}
 simple wrapper for code cleanup 
void sleepApp(int ms)
{
	std::this_thread::sleep_for(std::chrono::milliseconds(ms));
}
*/

int main(int argc, char **argv) {
	//
	std::string interface;
	interface = "can0";
	ctre::phoenix::platform::can::SetCANInterface(interface.c_str());
	initRobot();
	double targetVelocity = atof(argv[1]) * 60; // meters/minute
	//
	double flywheelRadius = 0.1524; // meters
	double friction = 1;
	double targetRPM = targetVelocity/(2*3.1415*flywheelRadius); // revolutions / minute
	double targetVelocity_100MS = targetRPM * 4096 / 600; // native units / 100ms
	
	auto startTime = std::chrono::steady_clock::now();
	auto currentTime = std::chrono::steady_clock::now();
	float totalTime = 60;
	float i=0;
	
	while (std::chrono::duration_cast<std::chrono::seconds>(currentTime - startTime).count() < totalTime) {
		ctre::phoenix::unmanaged::FeedEnable(100);
		tal.Set(ControlMode::Velocity, targetVelocity_100MS);
//tal.Set(ControlMode::PercentOutput, .2);
		
		/* yield for a bit */
		sleepApp(10);
		currentTime = std::chrono::steady_clock::now();
	}
	printf("end of while loop\n");
	tal.Set(ControlMode::PercentOutput, 0);
	return 0;
}
