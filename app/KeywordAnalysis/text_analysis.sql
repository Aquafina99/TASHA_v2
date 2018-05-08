-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: May 03, 2018 at 09:46 AM
-- Server version: 5.7.22-0ubuntu0.16.04.1-log
-- PHP Version: 7.0.28-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `text_analysis`
--

-- --------------------------------------------------------

--
-- Table structure for table `document`
--

CREATE TABLE `document` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `content` text NOT NULL,
  `dateline` varchar(255) DEFAULT NULL,
  `section` varchar(255) DEFAULT NULL,
  `byline` varchar(255) DEFAULT NULL,
  `journal` varchar(255) DEFAULT NULL,
  `doc_type` varchar(255) DEFAULT NULL,
  `publication_type` varchar(255) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `highlight` varchar(255) DEFAULT NULL,
  `question` varchar(255) DEFAULT NULL,
  `load_date` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `document_topics`
--

CREATE TABLE `document_topics` (
  `document_id` int(11) NOT NULL,
  `document_date` date DEFAULT NULL,
  `topic1_id` int(11) NOT NULL,
  `topic1_prob` float NOT NULL,
  `topic2_id` int(11) DEFAULT NULL,
  `topic2_prob` float DEFAULT NULL,
  `topic3_id` int(11) DEFAULT NULL,
  `topic3_prob` float DEFAULT NULL,
  `topic4_id` int(11) DEFAULT NULL,
  `topic4_prob` float DEFAULT NULL,
  `topic5_id` int(11) DEFAULT NULL,
  `topic5_prob` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `label` varchar(255) NOT NULL,
  `zoom_level` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `topic_term`
--

CREATE TABLE `topic_term` (
  `topic_id` int(11) NOT NULL,
  `term` varchar(100) NOT NULL,
  `term_prob` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `document`
--
ALTER TABLE `document`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `document_topics`
--
ALTER TABLE `document_topics`
  ADD PRIMARY KEY (`document_id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `topic_term`
--
ALTER TABLE `topic_term`
  ADD UNIQUE KEY `topic_id` (`topic_id`,`term`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
