package com.example.leomeynet.finalproject;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.os.AsyncTask;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.ArrayList;
import java.util.List;

import org.json.*;

public class MainActivity extends AppCompatActivity {
    private String ipAdd = "192.168.1.215";
    private String port = "10000";
    private InetAddress address;
    private DatagramSocket socket;
    private ReceiverTask receiverTask;
    private String tempItem;
    private Drawable tempImg;
    private TextView selectedItem;
    private ImageView selectedImg;
    private int nbClicks;
    private boolean srvOk = false;

    EditText ipSrv;
    EditText portSrv;
    TextView txtLeft;
    TextView txtMid;
    TextView txtRight;
    ImageView imgLeft;
    ImageView imgMid;
    ImageView imgRight;
    LinearLayout leftLayout;
    LinearLayout middleLayout;
    LinearLayout rightLayout;
    LinearLayout parentLayout;
    Button btnValidateSrv;
    Button btnSwap;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViews();

        ipSrv.setText(ipAdd, TextView.BufferType.EDITABLE);
        portSrv.setText(port, TextView.BufferType.EDITABLE);

        /*************** Listeners ******************/
        btnValidateSrv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ipAdd = ipSrv.getText().toString();
                port = portSrv.getText().toString();
                Toast.makeText(MainActivity.this, "Envois vers "+ipAdd+":"+port+" validé.\n", Toast.LENGTH_SHORT).show();
                try{
                    socket = new DatagramSocket();
                    address = InetAddress.getByName(ipAdd);
                    receiverTask = new ReceiverTask();
                    receiverTask.execute();
                }catch(IOException e){
                    e.printStackTrace();
                }
                srvOk = true;
            }
        });

        btnSwap.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if(srvOk) {
                    new Thread() {
                        @Override
                        public void run() {
                            StringBuilder sb = new StringBuilder();
                            sb.append(txtLeft.getText().charAt(0));
                            sb.append(txtMid.getText().charAt(0));
                            sb.append(txtRight.getText().charAt(0));
                            String dataSend = sb.toString();

                            byte[] dataToSend = dataSend.getBytes();

                            DatagramPacket data = new DatagramPacket(dataToSend, dataToSend.length, address, Integer.valueOf(port));
                            try {
                                socket.send(data);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }.start();
                }else{
                    Toast.makeText(MainActivity.this, "Validez le choix du serveur avant de continuer", Toast.LENGTH_SHORT).show();
                }
                if(srvOk) {
                    new Thread() {
                        @Override
                        public void run() {
                            String dataSend = "getValues()";

                            byte[] dataToSend = dataSend.getBytes();

                            DatagramPacket data = new DatagramPacket(dataToSend, dataToSend.length, address, Integer.valueOf(port));
                            try {
                                socket.send(data);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }.start();
                }
            }
        });

        leftLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nbClicks++;
                if(selectedItem == null && selectedImg == null && nbClicks < 2) {
                    selectedItem = txtLeft;
                    selectedImg = imgLeft;
                }else{
                    tempItem = selectedItem.getText().toString();
                    tempImg = selectedImg.getDrawable();

                    selectedItem.setText(txtLeft.getText());
                    selectedImg.setImageDrawable(imgLeft.getDrawable());

                    txtLeft.setText(tempItem);
                    imgLeft.setImageDrawable(tempImg);
                    nbClicks = 0;
                    selectedItem = null;
                    selectedImg = null;
                }
            }
        });

        middleLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nbClicks++;
                if(selectedItem == null && selectedImg == null && nbClicks < 2) {
                    selectedItem = txtMid;
                    selectedImg = imgMid;
                }else{
                    tempItem = selectedItem.getText().toString();
                    tempImg = selectedImg.getDrawable();

                    selectedItem.setText(txtMid.getText());
                    selectedImg.setImageDrawable(imgMid.getDrawable());

                    txtMid.setText(tempItem);
                    imgMid.setImageDrawable(tempImg);
                    nbClicks = 0;
                    selectedItem = null;
                    selectedImg = null;
                }
            }
        });

        rightLayout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                nbClicks++;
                if(selectedItem == null && selectedImg == null && nbClicks < 2) {
                    selectedItem = txtRight;
                    selectedImg = imgRight;
                }else{
                    tempItem = selectedItem.getText().toString();
                    tempImg = selectedImg.getDrawable();

                    selectedItem.setText(txtRight.getText());
                    selectedImg.setImageDrawable(imgRight.getDrawable());

                    txtRight.setText(tempItem);
                    imgRight.setImageDrawable(tempImg);
                    nbClicks = 0;
                    selectedItem = null;
                    selectedImg = null;
                }
            }
        });


    }

    //Associe les éléments de la vue à des variables accessibles.
    private void findViews() {
        ipSrv = findViewById(R.id.Ip);
        portSrv = findViewById(R.id.Port);

        txtLeft = findViewById(R.id.LeftTxt);
        txtMid = findViewById(R.id.MidTxt);
        txtRight = findViewById(R.id.RightTxt);

        imgLeft = findViewById(R.id.LeftImg);
        imgMid = findViewById(R.id.MidImg);
        imgRight = findViewById(R.id.RightImg);

        parentLayout = findViewById(R.id.dataLayout);
        leftLayout = findViewById(R.id.left_layout);
        middleLayout = findViewById(R.id.middle_layout);
        rightLayout = findViewById(R.id.right_layout);

        btnValidateSrv = findViewById(R.id.validateSrv);
        btnSwap = findViewById(R.id.SwapVal);
    }

    private class ReceiverTask extends AsyncTask <Void, byte[], Void> {
        protected Void doInBackground(Void... datas) {
            while (true) {
                byte[] data = new byte[1024]; // Espace de réception des données.
                DatagramPacket packet = new DatagramPacket(data, data.length);
                try {
                    System.out.println("Port "+socket.getLocalPort());
                    socket.receive(packet);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                int size = packet.getLength();
                onProgressUpdate(java.util.Arrays.copyOf(data, size));
            }
        }
        protected void onProgressUpdate(final byte[] data) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    // Appelé de manière asynchrone, mais synchronisé avec l’UI
                    char gauche = txtLeft.getText().charAt(0);
                    char mid = txtMid.getText().charAt(0);
                    char droite = txtRight.getText().charAt(0);
                    try {
                        JSONObject dataObj = new JSONObject(new String(data));
                        String lumi = dataObj.getString("Lux");
                        String temp = dataObj.getString("Temp");
                        String humi = dataObj.getString("Humidity");

                        switch (gauche){
                            case 'T':
                                txtLeft.setText("Température:\n"+temp+"°C");
                                break;
                            case 'H':
                                txtLeft.setText("Humidité:\n"+humi+"%");
                                break;
                            case 'L':
                                txtLeft.setText("Luminosité:\n"+lumi+" lux");
                                break;
                            default:
                                break;
                        }
                        switch (mid){
                            case 'T':
                                txtMid.setText("Température:\n"+temp+"°C");
                                break;
                            case 'H':
                                txtMid.setText("Humidité:\n"+humi+"%");
                                break;
                            case 'L':
                                txtMid.setText("Luminosité:\n"+lumi+" lux");
                                break;
                            default:
                                break;
                        }
                        switch (droite){
                            case 'T':
                                txtRight.setText("Température:\n"+temp+"°C");
                                break;
                            case 'H':
                                txtRight.setText("Humidité:\n"+humi+"%");
                                break;
                            case 'L':
                                txtRight.setText("Luminosité:\n"+lumi+" lux");
                                break;
                            default:
                                break;
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }
            });
        }
    }
}

