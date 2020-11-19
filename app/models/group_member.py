from app import db


group_member_table = db.Table("group_member",
                              db.Column("group_id",
                                        db.Integer,
                                        db.ForeignKey("group.id"),
                                        nullable=False),
                              db.Column("user_id",
                                        db.Integer,
                                        db.ForeignKey("user.id"),
                                        nullable=False))
