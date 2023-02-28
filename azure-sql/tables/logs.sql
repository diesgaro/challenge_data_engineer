CREATE TABLE [challenge].[logs](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[log_date_time] [datetime] NULL,
	[process] [varchar](50) NULL,
	[object_sended] [varchar](1000) NULL
) ON [PRIMARY]
GO
ALTER TABLE [challenge].[logs] ADD  DEFAULT (getdate()) FOR [log_date_time]
GO
