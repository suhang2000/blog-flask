-- --------------------------------------------------------
-- 主机:                           127.0.0.1
-- 服务器版本:                        8.0.20 - MySQL Community Server - GPL
-- 服务器操作系统:                      Win64
-- HeidiSQL 版本:                  10.3.0.5771
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- 导出 blogdb 的数据库结构
CREATE DATABASE IF NOT EXISTS `blogdb` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `blogdb`;

-- 导出  表 blogdb.admin 结构
CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` int NOT NULL AUTO_INCREMENT,
  `adminname` varchar(16) NOT NULL,
  `admin_password` varchar(16) NOT NULL,
  `official_name` varchar(255) DEFAULT NULL,
  `phone_number` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 正在导出表  blogdb.admin 的数据：~2 rows (大约)
DELETE FROM `admin`;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`admin_id`, `adminname`, `admin_password`, `official_name`, `phone_number`) VALUES
	(1, 'superuser01', '123456', 'Sam Chen', '9090980'),
	(2, 'superuser02', '123456', 'Angela Wang', '9090990');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- 导出  表 blogdb.blog 结构
CREATE TABLE IF NOT EXISTS `blog` (
  `blog_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `describe` varchar(300) DEFAULT NULL,
  `text` varchar(10000) DEFAULT NULL,
  `public_time` varchar(20) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`blog_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 正在导出表  blogdb.blog 的数据：~2 rows (大约)
DELETE FROM `blog`;
/*!40000 ALTER TABLE `blog` DISABLE KEYS */;
INSERT INTO `blog` (`blog_id`, `title`, `describe`, `text`, `public_time`, `user_id`) VALUES
	(1, 'This is not a test title', 'This is not a test description.', 'This is not a test text.', '2021-03-05 13:52:18', 10002),
	(2, 'This is a test title', 'This is a test description.', 'This is a test text.', '2021-01-01 23:54:29', 10001);
/*!40000 ALTER TABLE `blog` ENABLE KEYS */;

-- 导出  表 blogdb.comments 结构
CREATE TABLE IF NOT EXISTS `comments` (
  `comment_id` varchar(16) NOT NULL,
  `cblog_id` int NOT NULL,
  `cuser_id` int DEFAULT NULL,
  `content` varchar(200) DEFAULT NULL,
  `comment_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  KEY `blog_id` (`cblog_id`),
  KEY `user_id` (`cuser_id`),
  CONSTRAINT `blog_id` FOREIGN KEY (`cblog_id`) REFERENCES `blog` (`blog_id`) ON DELETE CASCADE,
  CONSTRAINT `user_id` FOREIGN KEY (`cuser_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 正在导出表  blogdb.comments 的数据：~2 rows (大约)
DELETE FROM `comments`;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;

-- 导出  表 blogdb.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL,
  `user_password` varchar(16) NOT NULL,
  `profile_photo` varchar(255) DEFAULT NULL,
  `gender` varchar(16) DEFAULT 'unkown',
  `phone_number` varchar(16) DEFAULT 'unkown',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

-- 正在导出表  blogdb.user 的数据：~2 rows (大约)
DELETE FROM `user`;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`user_id`, `username`, `user_password`, `profile_photo`, `gender`, `phone_number`) VALUES
	(13, '1', '2', '4', '4', '3'),
	(15, 'name', 'password', '23', 'female', '12345678910');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
