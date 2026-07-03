-- =====================================================================
-- IFQ582 Assignment 2  |  "League of Legends" group (Group 1D)
-- Indigenous Cultural Collection database
-- Build script for MySQL Workbench (MySQL 8.x)
--- =====================================================================

DROP DATABASE IF EXISTS ifq582_a2;
CREATE DATABASE ifq582_a2
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE ifq582_a2;

-- ---------------------------------------------------------------------
-- Tables (created in foreign-key dependency order)
-- ---------------------------------------------------------------------

CREATE TABLE Role (
    roleID          INT          NOT NULL AUTO_INCREMENT,
    roleName        VARCHAR(50)  NOT NULL,
    roleDescription VARCHAR(255) NULL,
    PRIMARY KEY (roleID)
) ENGINE=InnoDB;

CREATE TABLE Collection (
    collectionID          INT          NOT NULL AUTO_INCREMENT,
    collectionName        VARCHAR(150) NOT NULL,
    collectionDescription VARCHAR(500) NULL,
    collectionTheme       VARCHAR(100) NULL,
    PRIMARY KEY (collectionID)
) ENGINE=InnoDB;

CREATE TABLE AccessStatus (
    statusID          INT          NOT NULL AUTO_INCREMENT,
    statusName        VARCHAR(50)  NOT NULL,
    statusDescription VARCHAR(255) NULL,
    PRIMARY KEY (statusID)
) ENGINE=InnoDB;

CREATE TABLE `User` (
    userID        INT          NOT NULL AUTO_INCREMENT,
    roleID        INT          NOT NULL,
    fullName      VARCHAR(100) NULL,
    username      VARCHAR(50)  NOT NULL,
    email         VARCHAR(255) NOT NULL,
    passwordHash  VARCHAR(255) NOT NULL,
    accountStatus VARCHAR(20)  NOT NULL,
    createdDate   DATE         NULL,
    PRIMARY KEY (userID),
    UNIQUE KEY uq_user_username (username),
    UNIQUE KEY uq_user_email (email),
    CONSTRAINT fk_user_role
        FOREIGN KEY (roleID) REFERENCES Role (roleID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE CollectionItem (
    itemID         INT          NOT NULL AUTO_INCREMENT,
    collectionID   INT          NOT NULL,
    statusID       INT          NOT NULL DEFAULT 3,
    title          VARCHAR(200) NOT NULL,
    authorCreator  VARCHAR(150) NULL,
    `year`         SMALLINT     NULL,
    itemType       VARCHAR(50)  NULL,
    summary        VARCHAR(500) NULL,
    thumbnailPath  VARCHAR(255) NOT NULL DEFAULT 'uncatalogued-item.svg',
    nextReviewDate DATE         NULL,
    PRIMARY KEY (itemID),
    CONSTRAINT fk_item_collection
        FOREIGN KEY (collectionID) REFERENCES Collection (collectionID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_item_status
        FOREIGN KEY (statusID) REFERENCES AccessStatus (statusID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE CulturalMetadata (
    metadataID               INT          NOT NULL AUTO_INCREMENT,
    itemID                   INT          NOT NULL,
    communityGroup           VARCHAR(100) NULL,
    language                 VARCHAR(100) NULL,
    location                 VARCHAR(150) NULL,
    subjectArea              VARCHAR(100) NULL,
    culturalSensitivityNotes VARCHAR(500) NULL,
    culturalProtocolNotes    VARCHAR(500) NULL,
    accessRecommendations    VARCHAR(255) NULL,
    PRIMARY KEY (metadataID),
    UNIQUE KEY uq_metadata_item (itemID),      -- one row per CollectionItem (1 to 1)
    CONSTRAINT fk_metadata_item
        FOREIGN KEY (itemID) REFERENCES CollectionItem (itemID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE AccessRequest (
    requestID           INT          NOT NULL AUTO_INCREMENT,
    userID              INT          NOT NULL,
    itemID              INT          NOT NULL,
    requestReason       VARCHAR(500) NULL,
    supportingDocuments VARCHAR(255) NULL,
    requestDate         DATE         NULL,
    requestStatus       VARCHAR(20)  NOT NULL,
    PRIMARY KEY (requestID),
    CONSTRAINT fk_request_user
        FOREIGN KEY (userID) REFERENCES `User` (userID)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_request_item
        FOREIGN KEY (itemID) REFERENCES CollectionItem (itemID)
        ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ReviewDecision (
    decisionID       INT          NOT NULL AUTO_INCREMENT,
    requestID        INT          NOT NULL,
    reviewerID       INT          NOT NULL,    -- references User(userID)
    decisionType     VARCHAR(20)  NOT NULL,
    decisionNotes    VARCHAR(500) NULL,
    accessConditions VARCHAR(500) NULL,
    decisionDate     DATE         NULL,
    PRIMARY KEY (decisionID),
    CONSTRAINT fk_decision_request
        FOREIGN KEY (requestID) REFERENCES AccessRequest (requestID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_decision_reviewer
        FOREIGN KEY (reviewerID) REFERENCES `User` (userID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE CommunityComment (
    commentID   INT           NOT NULL AUTO_INCREMENT,
    requestID   INT           NOT NULL,
    reviewerID  INT           NOT NULL,    -- references User(userID)
    commentText VARCHAR(1000) NULL,
    createdDate DATE          NULL,
    PRIMARY KEY (commentID),
    CONSTRAINT fk_comment_request
        FOREIGN KEY (requestID) REFERENCES AccessRequest (requestID)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_comment_reviewer
        FOREIGN KEY (reviewerID) REFERENCES `User` (userID)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Sample data
-- ---------------------------------------------------------------------

INSERT INTO Role (roleID, roleName, roleDescription) VALUES
(1, 'Admin', 'Full system access; manages users, items and review decisions'),
(2, 'Community Reviewer/Elder', 'Reviews items under review; approves/rejects; updates cultural metadata'),
(3, 'Library Staff', 'Creates and edits items; uploads images and metadata'),
(4, 'Public User', 'Browses public items; views details; submits access requests');

INSERT INTO Collection (collectionID, collectionName, collectionDescription, collectionTheme) VALUES
(1, 'Languages of the Torres Strait', 'Dictionaries, recordings and books in Torres Strait languages', 'Language'),
(2, 'Songlines and Oral Histories', 'Recorded stories, songlines and community oral histories', 'Oral history'),
(3, 'Traditional Art and Craft', 'Photographs and records of weaving, painting and ceremony', 'Art and craft'),
(4, 'Bush Medicine and Knowledge Systems', 'Records of traditional plant knowledge, healing practices and seasonal calendars shared with community consent', 'Knowledge systems'),
(5, 'Caring for Country', 'Photographs, maps and stories documenting land and sea management practices across communities', 'Land and culture');

INSERT INTO AccessStatus (statusID, statusName, statusDescription) VALUES
(1, 'Open', 'Viewable by anyone; no access request needed'),
(2, 'Restricted', 'Requires an approved access request before viewing'),
(3, 'Culturally Sensitive', 'Requires an approved access request plus specific usage conditions (e.g. research use only, in-person viewing)');

-- Users 1 to 6 are active. Users 7 and 8 are inactive accounts kept for
-- login testing (an inactive admin and an inactive staff member).
INSERT INTO `User` (userID, roleID, fullName, username, email, passwordHash, accountStatus, createdDate) VALUES
(1, 1, 'Sarah Mitchell', 'smitchell', 's.mitchell@library.qut.edu.au', '$2b$12$Rk9...adminhash', 'active', '2025-11-01'),
(2, 3, 'James Okafor', 'jokafor', 'j.okafor@library.qut.edu.au', '$2b$12$Lp2...staffhash', 'active', '2025-12-02'),
(3, 2, 'Margaret Williams', 'mwilliams', 'm.williams@community.org.au', '$2b$12$Qa7...elderhash', 'active', '2025-08-09'),
(4, 2, 'David Yunupingu', 'dyunupingu', 'd.yunupingu@community.org.au', '$2b$12$Zx4...elderhash', 'active', '2025-05-05'),
(5, 4, 'Emily Chen', 'echen', 'emily.chen@gmail.com', '$2b$12$Bm1...publichash', 'active', '2025-09-09'),
(6, 4, 'Tom Harris', 'tharris', 'tom.harris@outlook.com', '$2b$12$Nv8...publichash', 'active', '2025-08-30'),
(7, 1, 'Michael Tan', 'mtan', 'm.tan@library.qut.edu.au', '$2b$12$Ab3...adminhash', 'inactive', '2025-01-15'),
(8, 3, 'Priya Singh', 'psingh', 'p.singh@library.qut.edu.au', '$2b$12$Rt6...staffhash', 'inactive', '2025-09-13');

INSERT INTO CollectionItem (itemID, collectionID, statusID, title, authorCreator, `year`, itemType, summary, thumbnailPath, nextReviewDate) VALUES
(1, 1, 1, 'Kalaw Lagaw Ya Dictionary', 'Torres Strait Language Centre', 2018, 'book', 'A community dictionary of the Kalaw Lagaw Ya language.', 'kalaw-lagaw-ya-dictionary.svg', NULL),
(2, 1, 2, 'Recordings of Meriam Mir Speakers', 'Dr Anne Foster', 2005, 'recording', 'Audio recordings of fluent Meriam Mir speakers.', 'recordings-of-meriam-mir-speakers.svg', '2026-11-15'),
(3, 2, 2, 'Creation Songline of the Seven Sisters', 'Recorded with community Elders', 1998, 'recording', 'A recorded songline shared under cultural protocol.', 'creation-songline-of-the-seven-sisters.svg', '2026-12-01'),
(4, 2, 1, 'Oral History: Mission Days', 'Community History Project', 2010, 'recording', 'Interviews recalling life on the missions.', 'oral-history-mission-days.svg', NULL),
(5, 3, 1, 'Weaving Patterns of the Yolngu', 'Buku-Larrnggay Mulka Centre', 2015, 'image', 'Photographs documenting traditional weaving patterns.', 'weaving-patterns-of-the-yolngu.svg', NULL),
(6, 3, 2, 'Ceremony Photographs Collection', 'Unknown photographer', 1972, 'image', 'A restricted set of ceremony photographs.', 'ceremony-photographs-collection.svg', '2026-09-20'),
(7, 1, 1, 'Children''s Picture Book in Yumplatok', 'Torres Strait Language Centre', 2020, 'book', 'An illustrated children''s book in Yumplatok (Torres Strait Creole).', 'childrens-picture-book-in-yumplatok.svg', NULL),
(8, 2, 2, 'Men''s Business Recordings', 'Recorded with community Elders', 1985, 'recording', 'Restricted recordings held under cultural protocol.', 'mens-business-recordings.svg', '2027-01-10'),
(9, 3, 1, 'Bark Painting Records', 'Arnhem Land Art Project', 2012, 'image', 'Catalogue of bark paintings with artist notes.', 'bark-painting-records.svg', NULL),
(10, 2, 3, 'Restricted Ceremony Audio', 'Recorded with community Elders', 1990, 'recording', 'Ceremony audio with an access request under assessment.', 'restricted-ceremony-audio.svg', '2026-08-05'),
(11, 1, 1, 'Yolngu Matha Language Primer', 'Yirrkala Community School', 2017, 'book', 'An introductory primer for Yolngu Matha.', 'yolngu-matha-language-primer.svg', NULL),
(12, 2, 2, 'Sacred Site Survey Notes', 'Heritage Survey Team', 2003, 'manuscript', 'Field notes referencing restricted sacred sites.', 'sacred-site-survey-notes.svg', '2026-10-30'),
(13, 3, 1, 'Community Festival Photographs', 'Community Media Unit', 2019, 'image', 'Photographs from annual community festivals.', 'community-festival-photographs.svg', NULL),
(14, 2, 3, 'Initiation Recordings', 'Recorded with community Elders', 1988, 'recording', 'Initiation recordings with an access request under assessment.', 'initiation-recordings.svg', '2026-08-05'),
(15, 2, 1, 'Dreaming Stories Anthology', 'Community Storytellers', 2014, 'book', 'A published anthology of Dreaming stories cleared for public access.', 'dreaming-stories-anthology.svg', NULL),
(16, 4, 1, 'Seasonal Plant Knowledge Cards', 'Community Health Project', 2021, 'resource', 'Illustrated cards describing traditional plant uses and seasonal gathering calendars, cleared for public education.', 'seasonal-plant-knowledge-cards.svg', NULL),
(17, 4, 3, 'Healing Practices Recordings', 'Recorded with senior knowledge holders', 1996, 'recording', 'Recordings of healing practices and plant preparation methods shared under specific cultural conditions.', 'healing-practices-recordings.svg', '2026-09-01'),
(18, 5, 1, 'Caring for Sea Country Photo Series', 'Coastal Rangers Program', 2022, 'image', 'Photographs documenting sea country management, ranger programs and community-led conservation work.', 'caring-for-sea-country-photo-series.svg', NULL),
(19, 5, 2, 'Land Management Oral Histories', 'Community History Project', 2009, 'recording', 'Interviews with Elders describing traditional land management and fire practices, access restricted pending family consent.', 'land-management-oral-histories.svg', '2026-10-15'),
(20, 2, 2, 'Recently Donated Community Recordings', 'Donated by community member', 2023, 'recording', 'Newly catalogued recordings awaiting cultural review before an access status is set.', 'recently-donated-community-recordings.svg', NULL);

INSERT INTO CulturalMetadata (metadataID, itemID, communityGroup, language, location, subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations) VALUES
(1, 1, 'Torres Strait Islander', 'Kalaw Lagaw Ya', 'Western Torres Strait', 'Language', 'None', 'Freely shareable for education', 'Open access'),
(2, 2, 'Torres Strait Islander', 'Meriam Mir', 'Murray Island', 'Language', 'Speakers'' families to be acknowledged', 'Permission of speakers'' descendants preferred', 'Approved request, research use'),
(3, 3, 'Central Desert', 'Pitjantjatjara', 'APY Lands', 'Songline', 'Women''s knowledge in parts', 'Share only with appropriate community members', 'Elder approval required'),
(4, 4, 'Torres Strait Islander', 'Yumplatok', 'Thursday Island', 'Oral history', 'None', 'Standard attribution', 'Open access'),
(5, 5, 'Yolngu', 'Yolngu Matha', 'Northeast Arnhem Land', 'Weaving', 'None', 'Acknowledge the art centre', 'Open access'),
(6, 6, 'Unknown', 'N/A', 'Unrecorded', 'Ceremony', 'Possible ceremony content; provenance unclear', 'Hold pending community identification', 'Approved request only'),
(7, 7, 'Torres Strait Islander', 'Yumplatok', 'Thursday Island', 'Children''s literature', 'None', 'Freely shareable for education', 'Open access'),
(8, 8, 'Central Desert', 'Arrernte', 'Central Australia', 'Ceremony', 'Men''s knowledge; highly restricted', 'Men''s business; access by senior men only', 'Elder approval required'),
(9, 9, 'Yolngu', 'Yolngu Matha', 'Arnhem Land', 'Painting', 'None', 'Acknowledge the artists', 'Open access'),
(10, 10, 'Central Desert', 'Warlpiri', 'Tanami', 'Ceremony', 'Ceremony content; restricted', 'Elder approval required before release', 'Approved request only'),
(11, 11, 'Yolngu', 'Yolngu Matha', 'Yirrkala', 'Language', 'None', 'Freely shareable for education', 'Open access'),
(12, 12, 'Multiple', 'N/A', 'Various', 'Sacred sites', 'Sacred site locations; sensitive', 'Do not disclose site coordinates', 'Approved request only'),
(13, 13, 'Mixed community', 'English', 'Regional Queensland', 'Community life', 'None', 'Standard attribution', 'Open access'),
(14, 14, 'Central Desert', 'Arrernte', 'Central Australia', 'Initiation', 'Initiation knowledge; highly restricted', 'Senior community members only', 'Elder approval required'),
(15, 15, 'Mixed community', 'English', 'Various', 'Oral history', 'None', 'Cleared for public release', 'Open access'),
(16, 16, 'Mixed community', 'English', 'Regional Queensland', 'Bush medicine', 'None', 'Standard attribution to contributing communities', 'Open access'),
(17, 17, 'Central Desert', 'Pitjantjatjara', 'APY Lands', 'Healing practices', 'Knowledge shared by senior holders only', 'Cultural protocol review required before any reuse', 'Elder approval required; research use only'),
(18, 18, 'Multiple coastal communities', 'English', 'Far North Queensland coast', 'Land and sea management', 'None', 'Acknowledge ranger program and community partners', 'Open access'),
(19, 19, 'Mixed community', 'English', 'Regional Queensland', 'Land management', 'Family names mentioned; consent to be confirmed', 'Hold pending family consent for named individuals', 'Approved request only, family consent pending');

-- AccessRequest 6 was added so every outcome has two examples. Its
-- rejection is recorded in ReviewDecision 4 (see the note at the top).
INSERT INTO AccessRequest (requestID, userID, itemID, requestReason, supportingDocuments, requestDate, requestStatus) VALUES
(1, 5, 2, 'PhD research on Meriam Mir language revival', 'ethics_approval_EC2026.pdf', '2026-05-20', 'Approved'),
(2, 6, 10, 'Family history research into community ceremonies', NULL, '2026-05-22', 'Pending'),
(3, 5, 6, 'Comparative study of historical photographs', 'ethics_approval_EC2026.pdf', '2026-05-25', 'Rejected'),
(4, 6, 14, 'Writing an article on initiation practices', 'media_brief.pdf', '2026-05-28', 'Pending'),
(5, 5, 12, 'Heritage research with community consent', 'consent_letter.pdf', '2026-06-01', 'Approved'),
(6, 6, 3, 'Personal interest', NULL, '2026-02-28', 'Rejected');

INSERT INTO ReviewDecision (decisionID, requestID, reviewerID, decisionType, decisionNotes, accessConditions, decisionDate) VALUES
(1, 1, 3, 'Approve', 'Ethics approval sighted; legitimate research use. Speakers'' families acknowledged.', 'Research use only, no reproduction without further permission', '2026-05-21'),
(2, 3, 4, 'Reject', 'Request does not meet the cultural protocol for these photographs. No specific need shown.', NULL, '2026-05-26'),
(3, 5, 3, 'Approve', 'Community consent letter provided; appropriate heritage research purpose.', 'View in reading room only; site coordinates redacted', '2026-06-02'),
(4, 6, 3, 'Reject', 'No specific need or community connection shown; personal interest does not meet the cultural protocol for this restricted songline.', NULL, '2026-03-02');

INSERT INTO CommunityComment (commentID, requestID, reviewerID, commentText, createdDate) VALUES
(1, 1, 3, 'Spoke with Meriam Mir community contacts about this use, they are comfortable with it provided families are acknowledged in any publication.', '2026-05-20'),
(2, 1, 4, 'Agree with Margaret. Recommend the acknowledgement condition is written into the decision.', '2026-05-21'),
(3, 2, 3, 'Need more detail on which community the requester is connected to before we can assess this fairly.', '2026-05-23'),
(4, 3, 4, 'These photographs include content that hasn''t been cleared for outside research use. Recommend declining.', '2026-05-25'),
(5, 4, 4, 'This touches men''s business. I''d like a second Elder''s view before we make a call.', '2026-05-29'),
(6, 4, 3, 'Agreed, flagging this for discussion at our next community reviewers'' meeting.', '2026-05-30'),
(7, 5, 3, 'Consent letter checks out. Happy to approve with the reading-room-only condition.', '2026-06-01'),
(8, 5, 4, 'Concur, and the site coordinates must stay redacted in any published material.', '2026-06-02');

-- ---------------------------------------------------------------------
-- Count check (Stage 0 pre-flight). Run this after the build.
-- Expected one row: 4, 5, 4, 8, 21, 19, 6, 4, 8
-- ---------------------------------------------------------------------
SELECT
  (SELECT COUNT(*) FROM Role)             AS roles,
  (SELECT COUNT(*) FROM Collection)       AS collections,
  (SELECT COUNT(*) FROM AccessStatus)     AS statuses,
  (SELECT COUNT(*) FROM `User`)           AS users,
  (SELECT COUNT(*) FROM CollectionItem)   AS items,
  (SELECT COUNT(*) FROM CulturalMetadata) AS metadata,
  (SELECT COUNT(*) FROM AccessRequest)    AS requests,
  (SELECT COUNT(*) FROM ReviewDecision)   AS decisions,
  (SELECT COUNT(*) FROM CommunityComment) AS comments;
