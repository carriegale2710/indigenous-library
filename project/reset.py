"""
Demo data reset for the Indigenous Collections System.

- Truncates the tables that a public demo visitor can actually write to (via registration, cataloguing, access requests, reviews, comments) 
- Reloads the fixed seed data from database.sql, so the live deployment doesn't accumulate visitor input over time.
- Lookup tables (Role, Collection, AccessStatus) are never touched here - they're static reference data, not something visitors write to.

Usage:
    From inside an app context (e.g. the /admin/reset-demo route):

        from project.reset import reset_demo_data
        reset_demo_data()

    As a one-off manual run:

        from project import create_app
        from project.reset import reset_demo_data
        app = create_app()
        with app.app_context():
            reset_demo_data()
"""
from project import mysql

# Truncated in child-to-parent FK order.
_RESET_TABLES = [
    "CommunityComment",
    "ReviewDecision",
    "AccessRequest",
    "CulturalMetadata",
    "CollectionItem",
    "`User`",
]

# Re-inserted in parent-to-child FK order (reverse of the truncate order).
# Copied verbatim from database.sql so the reset always returns to the
# exact same known-good state.
_SEED_STATEMENTS = [
    (
        "INSERT INTO `User` (userID, roleID, fullName, username, email, "
        "passwordHash, accountStatus, createdDate) VALUES "
        "(1, 1, 'Sarah Mitchell', 'smitchell', 's.mitchell@library.qut.edu.au', "
        "'$2b$12$Rk9...adminhash', 'active', '2025-11-01'), "
        "(2, 3, 'James Okafor', 'jokafor', 'j.okafor@library.qut.edu.au', "
        "'$2b$12$Lp2...staffhash', 'active', '2025-12-02'), "
        "(3, 2, 'Margaret Williams', 'mwilliams', 'm.williams@community.org.au', "
        "'$2b$12$Qa7...elderhash', 'active', '2025-08-09'), "
        "(4, 2, 'David Yunupingu', 'dyunupingu', 'd.yunupingu@community.org.au', "
        "'$2b$12$Zx4...elderhash', 'active', '2025-05-05'), "
        "(5, 4, 'Emily Chen', 'echen', 'emily.chen@gmail.com', "
        "'$2b$12$Bm1...publichash', 'active', '2025-09-09'), "
        "(6, 4, 'Tom Harris', 'tharris', 'tom.harris@outlook.com', "
        "'$2b$12$Nv8...publichash', 'active', '2025-08-30'), "
        "(7, 1, 'Michael Tan', 'mtan', 'm.tan@library.qut.edu.au', "
        "'$2b$12$Ab3...adminhash', 'inactive', '2025-01-15'), "
        "(8, 3, 'Priya Singh', 'psingh', 'p.singh@library.qut.edu.au', "
        "'$2b$12$Rt6...staffhash', 'inactive', '2025-09-13')"
    ),
    (
        "INSERT INTO CollectionItem (itemID, collectionID, statusID, title, "
        "authorCreator, `year`, itemType, summary, thumbnailPath, nextReviewDate) VALUES "
        "(1, 1, 1, 'Kalaw Lagaw Ya Dictionary', 'Torres Strait Language Centre', 2018, 'book', "
        "'A community dictionary of the Kalaw Lagaw Ya language.', 'kalaw-lagaw-ya-dictionary.webp', NULL), "
        "(2, 1, 2, 'Recordings of Meriam Mir Speakers', 'Dr Anne Foster', 2005, 'recording', "
        "'Audio recordings of fluent Meriam Mir speakers.', 'recordings-of-meriam-mir-speakers.webp', '2026-11-15'), "
        "(3, 2, 2, 'Creation Songline of the Seven Sisters', 'Recorded with community Elders', 1998, 'recording', "
        "'A recorded songline shared under cultural protocol.', 'creation-songline-of-the-seven-sisters.webp', '2026-12-01'), "
        "(4, 2, 1, 'Oral History: Mission Days', 'Community History Project', 2010, 'recording', "
        "'Interviews recalling life on the missions.', 'oral-history-mission-days.webp', NULL), "
        "(5, 3, 1, 'Weaving Patterns of the Yolngu', 'Buku-Larrnggay Mulka Centre', 2015, 'image', "
        "'Photographs documenting traditional weaving patterns.', 'weaving-patterns-of-the-yolngu.webp', NULL), "
        "(6, 3, 2, 'Ceremony Photographs Collection', 'Unknown photographer', 1972, 'image', "
        "'A restricted set of ceremony photographs.', 'ceremony-photographs-collection.webp', '2026-09-20'), "
        "(7, 1, 1, 'Children''s Picture Book in Yumplatok', 'Torres Strait Language Centre', 2020, 'book', "
        "'An illustrated children''s book in Yumplatok (Torres Strait Creole).', 'childrens-picture-book-in-yumplatok.webp', NULL), "
        "(8, 2, 2, 'Men''s Business Recordings', 'Recorded with community Elders', 1985, 'recording', "
        "'Restricted recordings held under cultural protocol.', 'mens-business-recordings.webp', '2027-01-10'), "
        "(9, 3, 1, 'Bark Painting Records', 'Arnhem Land Art Project', 2012, 'image', "
        "'Catalogue of bark paintings with artist notes.', 'bark-painting-records.webp', NULL), "
        "(10, 2, 3, 'Restricted Ceremony Audio', 'Recorded with community Elders', 1990, 'recording', "
        "'Ceremony audio with an access request under assessment.', 'restricted-ceremony-audio.webp', '2026-08-05'), "
        "(11, 1, 1, 'Yolngu Matha Language Primer', 'Yirrkala Community School', 2017, 'book', "
        "'An introductory primer for Yolngu Matha.', 'yolngu-matha-language-primer.webp', NULL), "
        "(12, 2, 2, 'Sacred Site Survey Notes', 'Heritage Survey Team', 2003, 'manuscript', "
        "'Field notes referencing restricted sacred sites.', 'sacred-site-survey-notes.webp', '2026-10-30'), "
        "(13, 3, 1, 'Community Festival Photographs', 'Community Media Unit', 2019, 'image', "
        "'Photographs from annual community festivals.', 'community-festival-photographs.webp', NULL), "
        "(14, 2, 3, 'Initiation Recordings', 'Recorded with community Elders', 1988, 'recording', "
        "'Initiation recordings with an access request under assessment.', 'initiation-recordings.webp', '2026-08-05'), "
        "(15, 2, 1, 'Dreaming Stories Anthology', 'Community Storytellers', 2014, 'book', "
        "'A published anthology of Dreaming stories cleared for public access.', 'dreaming-stories-anthology.webp', NULL), "
        "(16, 4, 1, 'Seasonal Plant Knowledge Cards', 'Community Health Project', 2021, 'resource', "
        "'Illustrated cards describing traditional plant uses and seasonal gathering calendars, cleared for public education.', "
        "'seasonal-plant-knowledge-cards.webp', NULL), "
        "(17, 4, 3, 'Healing Practices Recordings', 'Recorded with senior knowledge holders', 1996, 'recording', "
        "'Recordings of healing practices and plant preparation methods shared under specific cultural conditions.', "
        "'healing-practices-recordings.webp', '2026-09-01'), "
        "(18, 5, 1, 'Caring for Sea Country Photo Series', 'Coastal Rangers Program', 2022, 'image', "
        "'Photographs documenting sea country management, ranger programs and community-led conservation work.', "
        "'caring-for-sea-country-photo-series.webp', NULL), "
        "(19, 5, 2, 'Land Management Oral Histories', 'Community History Project', 2009, 'recording', "
        "'Interviews with Elders describing traditional land management and fire practices, access restricted pending family consent.', "
        "'land-management-oral-histories.webp', '2026-10-15'), "
        "(20, 2, 2, 'Recently Donated Community Recordings', 'Donated by community member', 2023, 'recording', "
        "'Newly catalogued recordings awaiting cultural review before an access status is set.', "
        "'recently-donated-community-recordings.webp', NULL)"
    ),
    (
        "INSERT INTO CulturalMetadata (metadataID, itemID, communityGroup, language, location, "
        "subjectArea, culturalSensitivityNotes, culturalProtocolNotes, accessRecommendations) VALUES "
        "(1, 1, 'Torres Strait Islander', 'Kalaw Lagaw Ya', 'Western Torres Strait', 'Language', 'None', "
        "'Freely shareable for education', 'Open access'), "
        "(2, 2, 'Torres Strait Islander', 'Meriam Mir', 'Murray Island', 'Language', "
        "'Speakers'' families to be acknowledged', 'Permission of speakers'' descendants preferred', "
        "'Approved request, research use'), "
        "(3, 3, 'Central Desert', 'Pitjantjatjara', 'APY Lands', 'Songline', 'Women''s knowledge in parts', "
        "'Share only with appropriate community members', 'Elder approval required'), "
        "(4, 4, 'Torres Strait Islander', 'Yumplatok', 'Thursday Island', 'Oral history', 'None', "
        "'Standard attribution', 'Open access'), "
        "(5, 5, 'Yolngu', 'Yolngu Matha', 'Northeast Arnhem Land', 'Weaving', 'None', "
        "'Acknowledge the art centre', 'Open access'), "
        "(6, 6, 'Unknown', 'N/A', 'Unrecorded', 'Ceremony', 'Possible ceremony content; provenance unclear', "
        "'Hold pending community identification', 'Approved request only'), "
        "(7, 7, 'Torres Strait Islander', 'Yumplatok', 'Thursday Island', 'Children''s literature', 'None', "
        "'Freely shareable for education', 'Open access'), "
        "(8, 8, 'Central Desert', 'Arrernte', 'Central Australia', 'Ceremony', "
        "'Men''s knowledge; highly restricted', 'Men''s business; access by senior men only', "
        "'Elder approval required'), "
        "(9, 9, 'Yolngu', 'Yolngu Matha', 'Arnhem Land', 'Painting', 'None', "
        "'Acknowledge the artists', 'Open access'), "
        "(10, 10, 'Central Desert', 'Warlpiri', 'Tanami', 'Ceremony', 'Ceremony content; restricted', "
        "'Elder approval required before release', 'Approved request only'), "
        "(11, 11, 'Yolngu', 'Yolngu Matha', 'Yirrkala', 'Language', 'None', "
        "'Freely shareable for education', 'Open access'), "
        "(12, 12, 'Multiple', 'N/A', 'Various', 'Sacred sites', 'Sacred site locations; sensitive', "
        "'Do not disclose site coordinates', 'Approved request only'), "
        "(13, 13, 'Mixed community', 'English', 'Regional Queensland', 'Community life', 'None', "
        "'Standard attribution', 'Open access'), "
        "(14, 14, 'Central Desert', 'Arrernte', 'Central Australia', 'Initiation', "
        "'Initiation knowledge; highly restricted', 'Senior community members only', "
        "'Elder approval required'), "
        "(15, 15, 'Mixed community', 'English', 'Various', 'Oral history', 'None', "
        "'Cleared for public release', 'Open access'), "
        "(16, 16, 'Mixed community', 'English', 'Regional Queensland', 'Bush medicine', 'None', "
        "'Standard attribution to contributing communities', 'Open access'), "
        "(17, 17, 'Central Desert', 'Pitjantjatjara', 'APY Lands', 'Healing practices', "
        "'Knowledge shared by senior holders only', 'Cultural protocol review required before any reuse', "
        "'Elder approval required; research use only'), "
        "(18, 18, 'Multiple coastal communities', 'English', 'Far North Queensland coast', "
        "'Land and sea management', 'None', 'Acknowledge ranger program and community partners', "
        "'Open access'), "
        "(19, 19, 'Mixed community', 'English', 'Regional Queensland', 'Land management', "
        "'Family names mentioned; consent to be confirmed', "
        "'Hold pending family consent for named individuals', "
        "'Approved request only, family consent pending')"
    ),
    (
        "INSERT INTO AccessRequest (requestID, userID, itemID, requestReason, supportingDocuments, "
        "requestDate, requestStatus) VALUES "
        "(1, 5, 2, 'PhD research on Meriam Mir language revival', 'ethics_approval_EC2026.pdf', "
        "'2026-05-20', 'Approved'), "
        "(2, 6, 10, 'Family history research into community ceremonies', NULL, '2026-05-22', 'Pending'), "
        "(3, 5, 6, 'Comparative study of historical photographs', 'ethics_approval_EC2026.pdf', "
        "'2026-05-25', 'Rejected'), "
        "(4, 6, 14, 'Writing an article on initiation practices', 'media_brief.pdf', '2026-05-28', 'Pending'), "
        "(5, 5, 12, 'Heritage research with community consent', 'consent_letter.pdf', '2026-06-01', 'Approved'), "
        "(6, 6, 3, 'Personal interest', NULL, '2026-02-28', 'Rejected')"
    ),
    (
        "INSERT INTO ReviewDecision (decisionID, requestID, reviewerID, decisionType, decisionNotes, "
        "accessConditions, decisionDate) VALUES "
        "(1, 1, 3, 'Approve', 'Ethics approval sighted; legitimate research use. Speakers'' families acknowledged.', "
        "'Research use only, no reproduction without further permission', '2026-05-21'), "
        "(2, 3, 4, 'Reject', 'Request does not meet the cultural protocol for these photographs. "
        "No specific need shown.', NULL, '2026-05-26'), "
        "(3, 5, 3, 'Approve', 'Community consent letter provided; appropriate heritage research purpose.', "
        "'View in reading room only; site coordinates redacted', '2026-06-02'), "
        "(4, 6, 3, 'Reject', 'No specific need or community connection shown; personal interest does not "
        "meet the cultural protocol for this restricted songline.', NULL, '2026-03-02')"
    ),
    (
        "INSERT INTO CommunityComment (commentID, requestID, reviewerID, commentText, createdDate) VALUES "
        "(1, 1, 3, 'Spoke with Meriam Mir community contacts about this use, they are comfortable with it "
        "provided families are acknowledged in any publication.', '2026-05-20'), "
        "(2, 1, 4, 'Agree with Margaret. Recommend the acknowledgement condition is written into the decision.', "
        "'2026-05-21'), "
        "(3, 2, 3, 'Need more detail on which community the requester is connected to before we can assess "
        "this fairly.', '2026-05-23'), "
        "(4, 3, 4, 'These photographs include content that hasn''t been cleared for outside research use. "
        "Recommend declining.', '2026-05-25'), "
        "(5, 4, 4, 'This touches men''s business. I''d like a second Elder''s view before we make a call.', "
        "'2026-05-29'), "
        "(6, 4, 3, 'Agreed, flagging this for discussion at our next community reviewers'' meeting.', "
        "'2026-05-30'), "
        "(7, 5, 3, 'Consent letter checks out. Happy to approve with the reading-room-only condition.', "
        "'2026-06-01'), "
        "(8, 5, 4, 'Concur, and the site coordinates must stay redacted in any published material.', "
        "'2026-06-02')"
    ),
]


def reset_demo_data():
    """
    Wipe every demo-writable table and reload the original seed data.

    Must be called from inside a Flask app context (mysql.connection needs
    an active app to bind to). Returns a small summary dict for logging.
    """
    cur = mysql.connection.cursor()

    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in _RESET_TABLES:
        cur.execute(f"TRUNCATE TABLE {table}")

    for statement in _SEED_STATEMENTS:
        cur.execute(statement)

    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    mysql.connection.commit()
    cur.close()

    return {"status": "ok", "tables_reset": len(_RESET_TABLES)}