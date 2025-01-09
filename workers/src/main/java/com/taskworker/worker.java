package com.taskworker;

import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DeliverCallback;

import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import java.nio.charset.StandardCharsets;

public class Worker {
    private static final String QUEUE_NAME = "task_queue";
    private static final String DB_URL = "jdbc:mysql://mysql:3306/task_scheduler";
    private static final String DB_USER = "root";
    private static final String DB_PASSWORD = "password";
    
    public static void main(String[] args) throws Exception {
        Class.forName("com.mysql.cj.jdbc.Driver");
        System.out.println("Worker is running...");

        java.sql.Connection dbConnection = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);

        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("rabbitmq");
        com.rabbitmq.client.Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();

        channel.queueDeclare(QUEUE_NAME, true, false, false, null);
        System.out.println("[*] Waiting for Messages - To exit press CTRL+C");

        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            String msg = new String(delivery.getBody(), java.nio.charset.StandardCharsets.UTF_8);
            System.out.println("[x] Received '" + msg + "'");

            int taskId = Integer.parseInt(msg.split(",")[0].split(":")[1]);
            updateTaskStatus(dbConnection, taskId, "in_progress");
            System.out.println("[x] Processing Task...");

            try{
                Thread.sleep(5000);
            }
            catch(Exception e){
                e.printStackTrace();
            }
            

            updateTaskStatus(dbConnection, taskId, "complete");
            System.out.println("[x] Task complete");
        };

        channel.basicConsume(QUEUE_NAME, true, deliverCallback, consumerTag -> {});
    }


    private static void updateTaskStatus(java.sql.Connection dbConnection, int taskId, String status) {
        try (PreparedStatement stmt = dbConnection.prepareStatement("UPDATE tasks SET status = ? WHERE id = ?")) {
            stmt.setString(1, status);
            stmt.setInt(2, taskId);
            stmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}