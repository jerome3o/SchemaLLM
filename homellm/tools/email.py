from typing import Optional

from langchain.tools import BaseTool
from langchain.llms.base import BaseLLM
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from pydantic import BaseModel, EmailStr
from googleapiclient.discovery import Resource

from homellm.google_services import send_email


class SendEmailParameters(BaseModel):
    subject: str
    body: str
    recipient: EmailStr


def get_email_parameters(input: str, llm: BaseLLM) -> SendEmailParameters:
    # Get the subject
    # Get the body
    # Get the recipient

    # Need to find a robust way of get these values from the llm, based on the input.
    # We can hard code for now, but a more general solution would be to do some jsonschema
    # validation

    return SendEmailParameters(
        subject="This is the subject of the email",
        body="This is the body of the email",
        recipient="",
    )


class SendEmailTool(BaseTool):
    name = "send_email"
    description = (
        "Useful for sending emails, a subject, body, and recipient are required."
    )
    gmail_service: Resource
    llm: BaseLLM

    def _run(
        self,
        input: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        inputs = get_email_parameters(input, self.llm)
        send_email(
            **inputs.dict(),
            gmail_service=self.gmail_service,
        )

    async def _arun(
        self,
        subject: str,
        body: str,
        recipient: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")