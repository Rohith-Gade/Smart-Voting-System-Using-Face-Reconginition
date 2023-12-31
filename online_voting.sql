-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 12, 2023 at 12:31 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `online_voting`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_id` int(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_id`, `name`, `email`, `password`) VALUES
(1, 'admin123', 'pendyalaspandana9@gmail.com', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `candidate`
--

CREATE TABLE `candidate` (
  `candidate_id` int(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `rollnumber` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `branch` varchar(10) NOT NULL,
  `semester` varchar(10) NOT NULL,
  `section` varchar(10) NOT NULL,
  `position` varchar(50) NOT NULL,
  `image` varchar(50) NOT NULL,
  `mobile` int(10) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `age` int(10) NOT NULL,
  `address` varchar(50) NOT NULL,
  `status` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `candidate`
--

INSERT INTO `candidate` (`candidate_id`, `name`, `rollnumber`, `email`, `password`, `branch`, `semester`, `section`, `position`, `image`, `mobile`, `gender`, `age`, `address`, `status`) VALUES
(18, 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', '1234', 'CSE', 'viii', 'Section-A', 'President', 'WIN_20230314_18_55_13_Pro_cUCAHcE.jpg', 2147483647, 'female', 22, '30-4-215,madikonda', 1),
(19, 'Spandu', '19281A0530', 'pendyalaspandana@gmail.com', '12345', 'CSE', 'vii', 'Section-B', 'President', 'WIN_20230313_17_50_59_Pro.jpg', 2147483647, 'female', 22, '30-4-215,madikonda', 1),
(20, 'shriya', '19281A0534', 'shriyakotoju@gmail.com', '1234', 'CSE', 'vii', 'Section-A', 'Vice-President', 'WIN_20230313_17_50_38_Pro.jpg', 2147483647, 'female', 33, '30-4-215,madikonda', 1),
(21, 'mammu', '19281A0534', 'shriyakotoj@gmail.com', '1234', 'CSE', 'viii', 'Section-B', 'Vice-President', 'WIN_20230313_17_51_03_Pro.jpg', 2147483647, 'female', 22, '30-4-215,madikonda', 1),
(22, 'chinni', '19281A0560', 'chinni@gmail.com', '1234', 'CSE', 'vi', 'Section-A', 'Secretary', 'WIN_20230313_17_48_54_Pro.jpg', 2147483647, 'female', 22, '30-4-215,madikonda', 1),
(23, 'lahari', '19281A0544', 'lahari@gmail.com', '1234', 'CSE', 'viii', 'Section-B', 'Treasurer', 'WIN_20230313_17_49_39_Pro.jpg', 2147483647, 'female', 33, '30-4-215,madikonda', 1),
(24, 'chinnu', '19281A0530', 'chinnu@gmail.com', '1234', 'CSE', 'iii', 'Section-A', 'Secretary', 'chinnu.jpg', 2147483647, 'Female', 22, 'mdk', 1),
(25, 'chinnu1', '19281A0530', 'chinn1u@gmail.com', '1234', 'CSE', 'iv', 'Section-A', 'Treasurer', 'chinnu1.jpg', 2147483647, 'Female', 22, 'mdk', 1);

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `firstname` varchar(50) NOT NULL,
  `lastname` varchar(11) NOT NULL,
  `rollnumber` varchar(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `message` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `firstname`, `lastname`, `rollnumber`, `email`, `message`) VALUES
(1, 'Spandana', '0', '19281A0530', 'pendyalaspandana9@gmail.com', 'hi'),
(2, 'Spandana', 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', 'hi'),
(3, 'kittu', 'kittu', '19281A0560', 'kittu@gmail.com', 'welcome'),
(4, 'kittu', 'kittu', '19281A0560', 'kittu@gmail.com', 'welcome'),
(5, 'kittu', 'kittu', '19281A0560', 'kittu@gmail.com', 'welcome'),
(6, 'Spandana', 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', '123'),
(7, 'Spandana', 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', '123'),
(8, 'Spandana', 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', '123'),
(9, 'chinni', 'chinni', '19281A0560', 'chinni@gmail.com', 'chinni'),
(10, 'Spandana', 'Spandana', '19281A0560', 'pendyalaspandana9@gmail.com', 'hiii');

-- --------------------------------------------------------

--
-- Table structure for table `election`
--

CREATE TABLE `election` (
  `electionid` int(50) NOT NULL,
  `electionname` varchar(20) NOT NULL,
  `starttime` time NOT NULL,
  `endtime` time NOT NULL,
  `voters` varchar(50) NOT NULL,
  `date` date NOT NULL,
  `status` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `election`
--

INSERT INTO `election` (`electionid`, `electionname`, `starttime`, `endtime`, `voters`, `date`, `status`) VALUES
(17, 'KCA', '19:34:00', '19:35:00', 'iii,iv,v', '2023-03-19', 0),
(18, 'KCA', '18:14:00', '20:14:00', 'i,ii,iii,iv', '2023-03-15', 0),
(20, 'KCA', '01:07:00', '23:58:00', 'ii,iii,iv', '2023-03-18', 0),
(21, 'KCA', '01:17:00', '23:59:00', 'ii,iii,iv,v,vi', '2023-03-19', 0),
(22, 'KCA', '14:54:00', '15:55:00', 'ii,iii,iv,v', '2023-04-12', 1);

-- --------------------------------------------------------

--
-- Table structure for table `forget`
--

CREATE TABLE `forget` (
  `email` varchar(50) NOT NULL,
  `otp` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `forget`
--

INSERT INTO `forget` (`email`, `otp`) VALUES
('pendyalaspandana9@gmail.com', 6106),
('pendyalaspandana9@gmail.com', 8330),
('pendyalaspandana9@gmail.com', 6622),
('pendyalaspandana9@gmail.com', 2578),
('pendyalaspandana9@gmail.com', 2903),
('keerthanapinigili560@gmail.com', 4480),
('keerthanapinigili560@gmail.com', 8470),
('keerthanapinigili560@gmail.com', 9953),
('pendyalaspandana9@gmail.com', 4907),
('pendyalaspandana9@gmail.com', 1988),
('pendyalaspandana9@gmail.com', 5860),
('pendyalaspandana9@gmail.com', 5562),
('pendyalaspandana9@gmail.com', 3025),
('pendyalaspandana9@gmail.com', 9119),
('pendyalaspandana9@gmail.com', 7660),
('pendyalaspandana9@gmail.com', 6276),
('pendyalaspandana9@gmail.com', 1411),
('pendyalaspandana9@gmail.com', 4142),
('pendyalaspandana9@gmail.com', 9909),
('shriyakotoju@gmail.com', 6421);

-- --------------------------------------------------------

--
-- Table structure for table `verify`
--

CREATE TABLE `verify` (
  `email` varchar(50) NOT NULL,
  `otp` int(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `verify`
--

INSERT INTO `verify` (`email`, `otp`) VALUES
('pendyalaspandana9@gmail.com', 7712),
('pendyalaspandana9@gmail.com', 2369),
('shriyakotoju@gmail.com', 2042),
('shriyakotoju@gmail.com', 5994),
('ksriya3105@gmail.com', 6256),
('allipravalika031@gmail.com', 9936),
('laharirikkala.111@gmail.com', 1108),
('keerthanapingili560@gmail.com', 2675),
('sriyakunkumalla@gmail.com', 3718);

-- --------------------------------------------------------

--
-- Table structure for table `voter`
--

CREATE TABLE `voter` (
  `studentid` int(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `rollnumber` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `branch` varchar(10) NOT NULL,
  `section` varchar(10) NOT NULL,
  `semester` varchar(10) NOT NULL,
  `mobile` int(10) NOT NULL,
  `image` varchar(50) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `age` int(10) NOT NULL,
  `address` text NOT NULL,
  `status` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voter`
--

INSERT INTO `voter` (`studentid`, `name`, `rollnumber`, `email`, `password`, `branch`, `section`, `semester`, `mobile`, `image`, `gender`, `age`, `address`, `status`) VALUES
(24, 'Spandana', '19281A0530', 'pendyalaspandana9@gmail.com', '1234', 'CSE', 'Section-A', 'iii', 2147483647, 'Spandana.jpg', 'female', 22, '30-4-215,madikonda', 1),
(27, 'shriya', '19281A0534', 'shriyakotoju@gmail.com', '1234', 'CSE', 'Section-A', 'iii', 2147483647, 'WIN_20230313_17_49_39_Pro_M8oxxBr.jpg', 'female', 22, '30-4-215,madikonda', 1),
(28, 'sriya', '19281A0504', 'ksriya3105@gmail.com', '1234', 'CSE', 'Section-A', 'iii', 2147483647, 'WIN_20230313_17_48_54_Pro_bVBN7RG.jpg', 'female', 22, '30-4-215,madikonda', 1),
(29, 'pravalika', '19281A0516', 'allipravalika031@gmail.com', '1234', 'CSE', 'Section-A', 'iv', 2147483647, 'WIN_20230313_17_49_39_Pro_Lz8jiIf.jpg', 'female', 22, '30-4-215,madikonda', 1),
(30, 'lahari', '19281A0544', 'laharirikkala.111@gmail.com', '1234', 'CSE', 'Section-A', 'iii', 2147483647, 'WIN_20230313_17_49_39_Pro_jBK8aai.jpg', 'female', 22, '30-4-215,madikonda', 1),
(31, 'kittu', '19281A0560', 'keerthanapingili560@gmail.com', '1234', 'CSE', 'Section-A', 'iv', 2147483647, 'WIN_20230313_17_49_39_Pro_ypMacdt.jpg', 'female', 22, '30-4-215,madikonda', 1),
(32, 'kittu', '19281A0544', 'sriyakunkumalla@gmail.com', '1234', 'CSE', 'Section-A', 'v', 2147483647, 'sriya.jpg', 'female', 22, '30-4-215,madikonda', 1);

-- --------------------------------------------------------

--
-- Table structure for table `voting`
--

CREATE TABLE `voting` (
  `id` int(50) NOT NULL,
  `electionid` int(50) NOT NULL,
  `studentid` int(50) NOT NULL,
  `president` varchar(50) NOT NULL,
  `vicepresident` varchar(50) NOT NULL,
  `secretary` varchar(50) NOT NULL,
  `treasurer` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voting`
--

INSERT INTO `voting` (`id`, `electionid`, `studentid`, `president`, `vicepresident`, `secretary`, `treasurer`) VALUES
(1, 20, 24, 'Spandana', 'shriya', 'chinni', 'lahari'),
(2, 20, 27, 'Spandana', 'shriya', 'chinni', 'lahari'),
(3, 20, 29, 'Spandana', 'shriya', 'chinni', 'lahari'),
(4, 20, 24, 'Spandu', 'mammu', 'chinni', 'lahari'),
(5, 20, 30, 'spandu', 'mammu', 'chinnu', 'chinnu1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `candidate`
--
ALTER TABLE `candidate`
  ADD PRIMARY KEY (`candidate_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `election`
--
ALTER TABLE `election`
  ADD PRIMARY KEY (`electionid`);

--
-- Indexes for table `voter`
--
ALTER TABLE `voter`
  ADD PRIMARY KEY (`studentid`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `voting`
--
ALTER TABLE `voting`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `candidate`
--
ALTER TABLE `candidate`
  MODIFY `candidate_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `election`
--
ALTER TABLE `election`
  MODIFY `electionid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `voter`
--
ALTER TABLE `voter`
  MODIFY `studentid` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `voting`
--
ALTER TABLE `voting`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
