# Migrate your database SQL dumps from MS SQL Server to PostgreSQL 

This script migrates INSERT queries from MS SQL Server format to PostgreSQL. You still have to create target tables by your own. Supports the dumps containing INSERTs for more than one table. Ignores anything besides of INSERTs.

## Sample input

```
EXEC sys.sp_addextendedproperty @name=N'ResultType', @value=N'0' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'tbluser', @level2type=N'COLUMN',@level2name=N'userid'
GO
EXEC sys.sp_addextendedproperty @name=N'Size', @value=N'4' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'tbluser', @level2type=N'COLUMN',@level2name=N'userid'
GO

... another weird shit goes here

INSERT [my_mapping_table] ([key], [value]) VALUES (27320, 10027350)

... and here

INSERT [my_mapping_table] ([key], [value]) VALUES (27320, 10027350)
```

## Sample output

```
INSERT INTO my_mapping_table (key, value)  VALUES
  (27320, 10027350),
  (27320, 10027350);
```

## RAM consumption

The converter uses Python generators so it does not load the whole dump into your RAM. This allows you to conver really huge dumps.
