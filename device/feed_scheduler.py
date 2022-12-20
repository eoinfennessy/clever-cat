from datetime import datetime, timedelta

class FeedScheduler:
    def __init__(self, feed_amount: float, feed_frequency: float, time_of_last_feed: datetime) -> None:
        self.feed_amount = feed_amount
        self.feed_frequency = timedelta(hours=feed_frequency)
        self.time_of_last_feed = time_of_last_feed

    def get_feed_amount_due(self) -> float:
        time_since_last_feed = datetime.now() - self.time_of_last_feed
        if time_since_last_feed > self.feed_frequency:
            return self.feed_amount
        else:
            return 0