-- Create the main database
CREATE DATABASE IF NOT EXISTS eduspark;
USE eduspark;

-- Create the users table
CREATE TABLE IF NOT EXISTS users (
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(255) NOT NULL UNIQUE,
password VARCHAR(255) NOT NULL,
is_premium BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the lessons table
CREATE TABLE IF NOT EXISTS lessons (
id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255) NOT NULL,
content TEXT NOT NULL,
is_premium BOOLEAN DEFAULT FALSE,
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some example free lessons
INSERT INTO lessons (title, content, is_premium) VALUES
('Introduction to Python', 'Python is a high-level, interpreted programming language known for its simplicity and readability...', FALSE),
('Basics of HTML', 'HTML, or HyperText Markup Language, is the standard markup language for documents designed to be displayed in a web browser...', FALSE),
('Understanding CSS', 'CSS stands for Cascading Style Sheets. It is used to style the look and feel of a website...', FALSE);

-- Insert a premium lesson (quiz)
INSERT INTO lessons (title, content, is_premium) VALUES
('Python Advanced Concepts Quiz', 'This quiz will test your knowledge of advanced Python concepts like decorators, generators, and asynchronous programming...', TRUE);