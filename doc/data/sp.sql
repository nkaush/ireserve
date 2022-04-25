CREATE PROCEDURE Compute_Ratings()
BEGIN
    DECLARE done int default 0;

    -- ====
    DECLARE currCustId INT;
    DECLARE currTPV INT;
    DECLARE currDiscountRate INT;
    DECLARE currOfferProductId INT;
    DECLARE currOfferPrice INT;
    -- ====

    -- DECLARE cur CURSOR FOR SELECT DISTINCT CustomerId, SUM(Price) AS TotalPurchaseValue
    --                         FROM Purchases
    --                         GROUP BY CustomerId
    --                         HAVING SUM(Price) >= 1000;

    DECLARE cur CURSOR FOR 
        SELECT * FROM 
        (SELECT `RoomID`, COUNT(`RoomID`) FROM `reservation` GROUP BY `RoomID`)

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    
    DROP TABLE IF EXISTS FinalTable;
    
    CREATE TABLE FinalTable (
         CustomerId INT PRIMARY KEY,
         OfferProductId INT,
         DiscountRate INT,
         OfferPrice INT
    );
    
    OPEN cur;
    
    REPEAT
        FETCH cur INTO currCustId, currTPV;
        
        IF (currTPV >= 2000) THEN 
            SET currDiscountRate = 90;
        ELSEIF (currTPV >= 1500) THEN
            SET currDiscountRate = 75;
        ELSE 
            SET currDiscountRate = 50;
        END IF;
            
        SET currOfferProductId = (SELECT pur.ProductId
                                  FROM Purchases pur
                                  WHERE pur.CustomerId = currCustId
                                  ORDER BY pur.Price DESC, pur.PurchaseId DESC
                                  LIMIT 1);
                                  
        SET currOfferPrice = FLOOR(currDiscountRate / 100 * (SELECT AVG(p.Price) FROM Purchases p
                                                             WHERE p.ProductId = currOfferProductId));
            
        INSERT IGNORE INTO FinalTable VALUES (currCustId, currOfferProductId, currDiscountRate, currOfferPrice);
    UNTIL done
    END REPEAT;
    
    SELECT * FROM FinalTable f ORDER BY f.CustomerId;
    
END