SELECT postID, COUNT(commentID) AS Kommentare
FROM comments
GROUP BY postID
ORDER BY COUNT(commentID) DESC
;
