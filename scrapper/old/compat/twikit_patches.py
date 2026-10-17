"""
Monkey-patch for twikit's SearchTimeline endpoint.

Includes adaptations of MIT-licensed third-party code.
See THIRD_PARTY_NOTICES.md and licenses/twikit-MIT.txt at the repository root.

Backports the SearchTimeline portion of upstream PR d60/twikit#419 (open at
time of writing). X rotated the SearchTimeline GraphQL doc_id, expanded the
required feature set, and added a `withGrokTranslatedBio` variable; without
all three in sync the endpoint returns 404 or HTTP 200 with an empty timeline.

The ondemand.s `KEY_BYTE` fix from the same PR is already covered locally by
`CompatibleClientTransaction`, so it's not duplicated here.

Remove this file once upstream releases a version with #419 merged.
"""
from twikit.client import gql as _gql
from twikit import user as _user_mod


_NEW_SEARCH_TIMELINE_QUERY_ID = "R0u1RWRf748KzyGBXvOYRA"


SEARCH_TIMELINE_FEATURES = {
    "rweb_video_screen_enabled": False,
    "rweb_cashtags_enabled": True,
    "profile_label_improvements_pcf_label_in_post_enabled": True,
    "responsive_web_profile_redirect_enabled": False,
    "rweb_tipjar_consumption_enabled": False,
    "verified_phone_label_enabled": False,
    "creator_subscriptions_tweet_preview_api_enabled": True,
    "responsive_web_graphql_timeline_navigation_enabled": True,
    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
    "premium_content_api_read_enabled": False,
    "communities_web_enable_tweet_community_results_fetch": True,
    "c9s_tweet_anatomy_moderator_badge_enabled": True,
    "responsive_web_grok_analyze_button_fetch_trends_enabled": False,
    "responsive_web_grok_analyze_post_followups_enabled": True,
    "responsive_web_jetfuel_frame": True,
    "responsive_web_grok_share_attachment_enabled": True,
    "responsive_web_grok_annotations_enabled": True,
    "articles_preview_enabled": True,
    "responsive_web_edit_tweet_api_enabled": True,
    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
    "view_counts_everywhere_api_enabled": True,
    "longform_notetweets_consumption_enabled": True,
    "responsive_web_twitter_article_tweet_consumption_enabled": True,
    "content_disclosure_indicator_enabled": True,
    "content_disclosure_ai_generated_indicator_enabled": True,
    "responsive_web_grok_show_grok_translated_post": True,
    "responsive_web_grok_analysis_button_from_backend": True,
    "post_ctas_fetch_enabled": True,
    "freedom_of_speech_not_reach_fetch_enabled": True,
    "standardized_nudges_misinfo": True,
    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
    "longform_notetweets_rich_text_read_enabled": True,
    "longform_notetweets_inline_media_enabled": False,
    "responsive_web_grok_image_annotation_enabled": True,
    "responsive_web_grok_imagine_annotation_enabled": True,
    "responsive_web_grok_community_note_auto_translation_is_enabled": True,
    "responsive_web_enhance_cards_enabled": False,
}


def _patched_search_timeline_endpoint() -> str:
    return _gql.Endpoint.url(f"{_NEW_SEARCH_TIMELINE_QUERY_ID}/SearchTimeline")


async def _patched_search_timeline(
    self,
    query: str,
    product: str,
    count: int,
    cursor: str | None,
):
    variables = {
        "rawQuery": query,
        "count": count,
        "querySource": "typed_query",
        "product": product,
        "withGrokTranslatedBio": True,
    }
    if cursor is not None:
        variables["cursor"] = cursor
    return await self.gql_get(
        _gql.Endpoint.SEARCH_TIMELINE,
        variables,
        SEARCH_TIMELINE_FEATURES,
    )


_original_user_init = _user_mod.User.__init__


def _patched_user_init(self, client, data: dict) -> None:
    """X movió `created_at`, `name`, `screen_name` y la imagen de perfil
    fuera de `legacy` a sub-objetos nuevos (`core`, `avatar`). El __init__
    original peta con KeyError sobre esos campos y twikit lo traga en
    silencio en search_tweet, devolviendo 0 resultados.

    Sintetizamos un `legacy` con los campos faltantes desde el nuevo shape
    y rellenamos defaults para los demás keys que X omite intermitentemente
    (issues #417/#425). Después delegamos al constructor original.
    """
    data = dict(data) if data is not None else {}
    legacy = dict(data.get("legacy") or {})
    core = data.get("core") or {}
    avatar = data.get("avatar") or {}
    dm_permissions = data.get("dm_permissions") or {}
    media_permissions = data.get("media_permissions") or {}
    location = data.get("location") or {}

    legacy.setdefault("created_at", core.get("created_at", ""))
    legacy.setdefault("name", core.get("name", ""))
    legacy.setdefault("screen_name", core.get("screen_name", ""))
    legacy.setdefault("profile_image_url_https", avatar.get("image_url", ""))

    legacy.setdefault("location", location.get("location", ""))
    legacy.setdefault("description", "")
    entities = dict(legacy.get("entities") or {})
    description_entities = dict(entities.get("description") or {})
    description_entities.setdefault("urls", [])
    entities["description"] = description_entities
    legacy["entities"] = entities

    legacy.setdefault("pinned_tweet_ids_str", [])
    legacy.setdefault("verified", False)
    legacy.setdefault("possibly_sensitive", False)
    legacy.setdefault("can_dm", dm_permissions.get("can_dm", False))
    legacy.setdefault(
        "can_media_tag",
        media_permissions.get("can_media_tag", False),
    )
    legacy.setdefault("want_retweets", False)
    legacy.setdefault("default_profile", False)
    legacy.setdefault("default_profile_image", False)
    legacy.setdefault("has_custom_timelines", False)
    legacy.setdefault("fast_followers_count", 0)
    legacy.setdefault("normal_followers_count", 0)
    legacy.setdefault("friends_count", 0)
    legacy.setdefault("favourites_count", 0)
    legacy.setdefault("listed_count", 0)
    legacy.setdefault("media_count", 0)
    legacy.setdefault("statuses_count", 0)
    legacy.setdefault("is_translator", False)
    legacy.setdefault("translator_type", "none")
    legacy.setdefault("withheld_in_countries", [])

    data["legacy"] = legacy
    data.setdefault("is_blue_verified", False)

    _original_user_init(self, client, data)


def apply() -> None:
    _gql.Endpoint.SEARCH_TIMELINE = _patched_search_timeline_endpoint()
    _gql.GQLClient.search_timeline = _patched_search_timeline
    _user_mod.User.__init__ = _patched_user_init
