import re

from twikit.x_client_transaction import ClientTransaction


LEGACY_ON_DEMAND_FILE_REGEX = re.compile(
    r"""['"]ondemand\.s['"]\s*:\s*['"]([\w-]+)['"]"""
)
CHUNK_NAME_REGEX = re.compile(
    r"""['"]?(\d+)['"]?\s*:\s*['"]ondemand\.s['"]"""
)
KEY_BYTE_INDEX_REGEX = re.compile(
    r"""\(\w+\[(\d{1,2})\],\s*16\)"""
)


class CompatibleClientTransaction(ClientTransaction):
    async def get_indices(self, home_page_response, session, headers):
        response = self.validate_response(home_page_response)
        response_text = str(response)

        legacy_match = LEGACY_ON_DEMAND_FILE_REGEX.search(response_text)
        file_hash = legacy_match.group(1) if legacy_match else None

        if file_hash is None:
            chunk_match = CHUNK_NAME_REGEX.search(response_text)
            if chunk_match:
                chunk_id = re.escape(chunk_match.group(1))
                hash_pattern = re.compile(
                    rf"""['"]?{chunk_id}['"]?\s*:\s*['"]([\w-]+)['"]"""
                )
                for match in hash_pattern.finditer(response_text):
                    candidate = match.group(1)
                    if candidate != "ondemand.s":
                        file_hash = candidate
                        break

        if file_hash is None:
            raise RuntimeError("No se pudo localizar el recurso ondemand.s de X")

        url = (
            "https://abs.twimg.com/responsive-web/client-web/"
            f"ondemand.s.{file_hash}a.js"
        )
        on_demand_response = await session.request(
            method="GET",
            url=url,
            headers=headers,
        )
        on_demand_response.raise_for_status()

        indices = [
            int(match.group(1))
            for match in KEY_BYTE_INDEX_REGEX.finditer(on_demand_response.text)
        ]
        if not indices:
            raise RuntimeError(
                "No se pudieron obtener los índices de transacción de X"
            )

        return indices[0], indices[1:]
