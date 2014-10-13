package com.example.lightmeup;

import android.app.Activity;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity implements SensorEventListener {
	SensorManager sm;
	Sensor lightSensor;
	TextView tv1, tv2, tv3;
	boolean OneTimeFlag = true;
	String uri = "http://malelm.com/action.php?" ;
	String checkIfSameAction = "nothing";
	String action = "nothing";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		tv1 = (TextView) findViewById(R.id.textView1);
		tv2 = (TextView) findViewById(R.id.textView2);
		tv3 = (TextView) findViewById(R.id.textView3);

		sm = (SensorManager) getSystemService(SENSOR_SERVICE);
		lightSensor = sm.getDefaultSensor(Sensor.TYPE_LIGHT);
	}

	@Override
	protected void onResume() {
		super.onResume();
		sm.registerListener(this, lightSensor,
				SensorManager.SENSOR_DELAY_NORMAL);
	}

	@Override
	protected void onPause() {
		super.onPause();
		sm.unregisterListener(this);
	}

	@Override
	public void onAccuracyChanged(Sensor arg0, int arg1) {

	}

	@Override
	public void onSensorChanged(SensorEvent light) {

			if (isOnline()) {

				if (light.values[0] < 3000) {
				//	tv3.setText("Action : Full open");
					uri += "action=fullopen";
					checkIfSameAction = "fullopen" ;
				} else if (light.values[0] > 3000 && light.values[0] < 5000) {
				//	tv3.setText("Action : Half open");
					uri += "action=halfopen";
					checkIfSameAction = "halfopen" ;
				} else {
				//	tv3.setText("Action : Close");
					uri += "action=close";
					checkIfSameAction = "close" ;
				}

				if(checkIfSameAction != action ){
					 action = checkIfSameAction ;
					TaskSend task = new TaskSend();
					task.executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR,uri);
				}
			} else {
				Toast.makeText(this, "Network is not available",
						Toast.LENGTH_LONG).show();
			}
			tv1.setText("Light Sensor values : " + light.values[0]);
			tv2.setText("Max value range : " + lightSensor.getMaximumRange());	
	}


	// Check for network connectivity
	protected boolean isOnline() {
		ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
		NetworkInfo netInfo = cm.getActiveNetworkInfo();

		if (netInfo != null && netInfo.isConnectedOrConnecting()) {
			return true;
		} else {
			return false;
		}
	}

	// Using AsycTask to make a call over the network
	private class TaskSend extends AsyncTask<String, String, String> {

		@Override
		protected String doInBackground(String... params) {
			
			return HttpManager.sendData(params[0]);
		}
		
		@Override
		protected void onPostExecute(String result) {
			tv3.setText(result);
		}
	}
}
