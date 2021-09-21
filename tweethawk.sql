-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-09-2021 a las 15:46:36
-- Versión del servidor: 10.4.16-MariaDB
-- Versión de PHP: 7.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tweethawk`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitorizegroups`
--

CREATE TABLE `monitorizegroups` (
  `ID` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `description` varchar(100) NOT NULL,
  `looptime` int(11) NOT NULL DEFAULT 15,
  `nUsers` int(11) NOT NULL DEFAULT 0,
  `nRules` int(11) NOT NULL DEFAULT 0,
  `nResults` int(11) NOT NULL DEFAULT 0,
  `lastTimeScanned` datetime DEFAULT NULL,
  `nextTimeScan` datetime NOT NULL DEFAULT current_timestamp(),
  `autorun` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitorizegroupsettings`
--

CREATE TABLE `monitorizegroupsettings` (
  `groupID` int(11) NOT NULL,
  `slackToken` varchar(150) NOT NULL,
  `slackgroupID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitorizeresults`
--

CREATE TABLE `monitorizeresults` (
  `groupID` int(11) NOT NULL,
  `userID` bigint(20) NOT NULL,
  `ruleID` int(11) NOT NULL,
  `new` tinyint(1) NOT NULL,
  `tweetID` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `tweet` varchar(300) COLLATE utf8mb4_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Disparadores `monitorizeresults`
--
DELIMITER $$
CREATE TRIGGER `update_nResults_Group` AFTER INSERT ON `monitorizeresults` FOR EACH ROW BEGIN
    SET @nResults = ((SELECT nResults FROM monitorizegroups WHERE ID = NEW.groupID) + 1);
    UPDATE monitorizegroups SET nResults = @nResults  WHERE ID = NEW.groupID;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitorizerules`
--

CREATE TABLE `monitorizerules` (
  `ID` int(11) NOT NULL,
  `groupID` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  `rule` varchar(50) NOT NULL,
  `priority` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Disparadores `monitorizerules`
--
DELIMITER $$
CREATE TRIGGER `update_nRules_Group` AFTER INSERT ON `monitorizerules` FOR EACH ROW BEGIN
    SET @nRules = ((SELECT nRules FROM monitorizegroups WHERE ID = NEW.groupID) + 1);
    UPDATE monitorizegroups SET nRules = @nRules  WHERE ID = NEW.groupID;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `monitorizeusers`
--

CREATE TABLE `monitorizeusers` (
  `userID` bigint(20) NOT NULL,
  `groupID` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `lastTweetCursor` varchar(30) NOT NULL,
  `profilePicURL` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Disparadores `monitorizeusers`
--
DELIMITER $$
CREATE TRIGGER `update_nUsers_Group` AFTER INSERT ON `monitorizeusers` FOR EACH ROW BEGIN
    SET @nUsers = ((SELECT nUsers FROM monitorizegroups WHERE ID = NEW.groupID) + 1);
    UPDATE monitorizegroups SET nUsers = @nUsers  WHERE ID = NEW.groupID;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `settings`
--

CREATE TABLE `settings` (
  `autorunMonitor` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `settings`
--

INSERT INTO `settings` (`autorunMonitor`) VALUES
(0);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `monitorizegroups`
--
ALTER TABLE `monitorizegroups`
  ADD PRIMARY KEY (`ID`);

--
-- Indices de la tabla `monitorizegroupsettings`
--
ALTER TABLE `monitorizegroupsettings`
  ADD PRIMARY KEY (`groupID`);

--
-- Indices de la tabla `monitorizeresults`
--
ALTER TABLE `monitorizeresults`
  ADD KEY `groupID` (`groupID`),
  ADD KEY `ruleID` (`ruleID`);

--
-- Indices de la tabla `monitorizerules`
--
ALTER TABLE `monitorizerules`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `groupID` (`groupID`,`type`,`rule`);

--
-- Indices de la tabla `monitorizeusers`
--
ALTER TABLE `monitorizeusers`
  ADD UNIQUE KEY `userID` (`userID`,`groupID`),
  ADD KEY `monitorizeusers_ibfk_1` (`groupID`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `monitorizegroups`
--
ALTER TABLE `monitorizegroups`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `monitorizerules`
--
ALTER TABLE `monitorizerules`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `monitorizeresults`
--
ALTER TABLE `monitorizeresults`
  ADD CONSTRAINT `monitorizeresults_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `monitorizegroups` (`ID`),
  ADD CONSTRAINT `monitorizeresults_ibfk_2` FOREIGN KEY (`ruleID`) REFERENCES `monitorizerules` (`ID`);

--
-- Filtros para la tabla `monitorizerules`
--
ALTER TABLE `monitorizerules`
  ADD CONSTRAINT `monitorizerules_ibfk_1` FOREIGN KEY (`groupID`) REFERENCES `monitorizegroups` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
