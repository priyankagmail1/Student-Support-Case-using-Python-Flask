-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/--
-- Host: 127.0.0.1


SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



INSERT INTO `admin` (`id`, `email`, `password`) VALUES
(1, 'user@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8');



CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `desc` longtext NOT NULL,
  `author` varchar(255) NOT NULL,
  `availability` tinyint(1) NOT NULL,
  `edition` varchar(255) NOT NULL,
  `count` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



INSERT INTO `books` (`id`, `name`, `desc`, `author`, `availability`, `edition`, `count`) VALUES
(1, '101 Ways To Be A Software Engineer', 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Aut repudiandae assumenda distinctio quas tempore, voluptatibus accusamus dolores temporibus, recusandae eligendi similique. Optio, eius? Sint vel nemo, quisquam architecto fugit odio!', 'Mr. Johnny Test', 1, '1', 3),
(2, 'JAVA For Absolute Beginners', 'Step into the basics of java programmming along with globally famed programmer', '', 1, '1', 5);



CREATE TABLE `reserve` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



INSERT INTO `reserve` (`id`, `user_id`, `book_id`) VALUES
(1, 1, 1),
(2, 6, 1);



CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `password` varchar(1000) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `bio` longtext COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `mob` varchar(255) COLLATE utf8mb4_unicode_520_ci NOT NULL,
  `lock` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_520_ci;



INSERT INTO `users` (`id`, `name`, `email`, `password`, `bio`, `mob`, `lock`, `created_at`) VALUES
(1, 'user1', 'user@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'They watch you from the shelf while you sleep 👀. Are you dreaming of them, they wonder, in that wistful mood books are prone to at night when they’re bored and there’s nothing else to do but tease the cat.?', '', 0, '2021-11-09 00:00:00'),
(6, 'Alice bob', 'Alice@gmail.com', '025db420560617303c2ba988d050ec62562343bc0fb0358d31d2f0bae8dbede8', 'Hi :)! Long time no see ❤️', '', 0, '2021-11-18 23:07:53');


ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `reserve`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;


ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;


ALTER TABLE `reserve`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;


ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
COMMIT;

