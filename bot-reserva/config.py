#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3979
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    API_BASE_URL = "http://localhost:8080/api" 
    CLU_ENDPOINT = "https://hotelbotreservatipon.cognitiveservices.azure.com/"
    CLU_KEY = "2xjNBtRtzlukP2Advie631EeArdLABWBEKd1LylNbSZni0IFgHhsJQQJ99BKACHYHv6XJ3w3AAAaACOGuRki"
    CLU_PROJECT = "HotelReservation"
    CLU_DEPLOYMENTNAME = "HotelReservation"