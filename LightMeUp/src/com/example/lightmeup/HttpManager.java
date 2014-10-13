package com.example.lightmeup;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class HttpManager {
	public static String sendData(String uri){
		BufferedReader reader = null ;
		try {
			URL url = new URL(uri);
			HttpURLConnection con = (HttpURLConnection) url.openConnection();
		
			// Getting a response for testing
			
		    reader = new BufferedReader( new InputStreamReader( con.getInputStream()));
			return reader.readLine();
			
			
		} catch (Exception e) {
			if(reader !=null){
				try {
					reader.close();
				} catch (IOException e1) {
					e1.printStackTrace();
				}
			}
			return "A problem with data !";
		}
	}
}
