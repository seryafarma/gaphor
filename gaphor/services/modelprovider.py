from typing import Dict

from gaphor.abc import ModelProvider, Service
from gaphor.entrypoint import initialize


class ModelProviderService(Service, ModelProvider):

    DEFAULT_PROFILE = "UML"

    def __init__(self, properties={}):
        """
        Create a new Model Provider. It will provide all models defined
        as entrypoints under `[gaphor.modelproviders]`.

        Te `properties` argument is optional, in which case the service will
        default to UML.
        """
        self.model_providers: Dict[str, ModelProvider] = initialize(
            "gaphor.modelproviders"
        )
        self.properties = properties

    def shutdown(self):
        pass

    @property
    def active_provider(self):
        profile = self.properties.get("profile", default=self.DEFAULT_PROFILE)
        if profile not in self.model_providers:
            profile = self.DEFAULT_PROFILE
        return self.model_providers[profile]

    @property
    def name(self):
        return self.active_provider.name

    def lookup_element(self, name):
        return self.first(lambda provider: provider.lookup_element(name))

    def lookup_diagram_item(self, name):
        return self.first(lambda provider: provider.lookup_diagram_item(name))

    def toolbox_definition(self):
        return self.active_provider.toolbox_definition

    def first(self, predicate):
        for _, provider in self.model_providers.items():
            type = predicate(provider)
            if type:
                return type