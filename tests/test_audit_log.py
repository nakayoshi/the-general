import unittest
from datetime import datetime
from dataclasses import dataclass

from discord import Embed

from logic.audit_log import ServerLogImpl, NoActionError


@dataclass
class User:
    name: str
    avatar_url: str


class TestCreateEmbed(unittest.TestCase):
    def setUp(self):
        self.sample_embed = Embed()
        self.user = User("chun", "https://example.com/icon.png")
        self.channel_name = "test_channel"
        self.created_at = datetime.now()

    def test_dispatch(self):
        with self.assertRaises(NoActionError):
            ServerLogImpl.create_log_embed("no_exist")
        self.assertIsNotNone(
            ServerLogImpl.create_log_embed(
                "channel", "create", self.user, self.channel_name, self.created_at
            )
        )

    def test_create_channel_embed(self):
        title = "チャンネルが作成されました"
        color = 0x5CB85C

        implemented_embed = ServerLogImpl._channel(
            "create", self.user, self.channel_name, self.created_at
        )

        self.assertEqual(implemented_embed.title, title)
        self.assertEqual(implemented_embed.color.value, color)
        self.assertEqual(implemented_embed.timestamp, self.created_at)
        self.assertEqual(implemented_embed.author.name, self.user.name)
        self.assertEqual(implemented_embed.author.icon_url, self.user.avatar_url)

        self.assertEqual(len(implemented_embed.fields), 1)
        channel_field = implemented_embed.fields[0]
        self.assertEqual(channel_field.name, "チャンネル")
        self.assertEqual(channel_field.value, self.channel_name)
        self.assertTrue(channel_field.inline)
