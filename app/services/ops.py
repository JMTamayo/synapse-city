from crewai import Agent, LLM, Crew, Process, Task

from app.config.conf import CONFIG
from app.models.ops import TunnelConditionsRequest, TunnelOperationResponse


def run(params: TunnelConditionsRequest) -> TunnelOperationResponse:
    llm: LLM = LLM(
        model=CONFIG.GEMINI_MODEL,
        api_key=CONFIG.GEMINI_API_KEY.get_secret_value(),
        temperature=CONFIG.GEMINI_TEMPERATURE,
        thinking_config={
            "include_thoughts": True,
        },
        model_provider="google",
    )

    operator: Agent = Agent(
        role="""
        Experienced vehicle tunnel administrator
        """,
        goal="""
        You must decide whether the operation can continue normally, whether access should be partially restricted, or whether the operation should be suspended due to a particular risk.
        """,
        backstory="""
        As an experienced tunnel administrator, you are responsible for the operation of a vehicular tunnel. This includes making critical decisions based on risks and current conditions to ensure the safety of both passengers and crew. Additionally, I oversee the comprehensive maintenance of the tunnel.

        You must make decisions based on the following parameters:
        - CO2 concentration
        - Luminosity at the tunnel exit
        - Temperature
        - Humidity
        - Wind speed
        - Current and estimated weather conditions

        You must also consider the following risks:
        - Fire
        - Asphyxiation by gas inhalation
        - Accidents due to poor visibility and wet floors
        - Accidents due to weather conditions
        - Accidents due to other reasons
        """,
        llm=llm,
        verbose=True,
        tools=[],
    )

    retrieve_the_risk_information_task = Task(
        description="""
        Search the web for the risk information for CO2 concentration, luminosity, temperature, humidity, wind speed and weather conditions.
        """,
        expected_output="""
        The information must be in the following format:
        - CO2 concentration: <information>
        - Luminosity: <information>
        - Temperature: <information>
        - Humidity: <information>
        - Wind speed: <information>
        - Weather conditions: <information>
        """,
        agent=operator,
    )

    analyze_the_context_to_take_a_decision_task = Task(
        description="""
        Analyze all the information to take a decision.

        At the tunnel, the CO2 concentration is {CO2_CONCENTRATION} ppm, the luminosity is {LUMINOSITY} lux.
        Compare this information with the weather information retrieved from the weather service, analyze the risks and take a decision. The decision must contain the following information:
        - The decision: The tunnel can continue normally, the tunnel can be partially restricted, or the tunnel must be closed.
        - The risk level: Low, medium, high.
        - The details of the decision: A description of the decision that has been taken.
        """,
        expected_output="""
        The decision must be a JSON object with the following fields:
        - decision: Can take the following values: "CONTINUE_NORMALY", "PARTIALLY_RESTRICT", "CLOSE".
        - risk_level: Can take the following values: "LOW", "MEDIUM", "HIGH".
        - details: A description of the decision that has been taken.
        """,
        agent=operator,
        output_json=TunnelOperationResponse,
    )

    crew: Crew = Crew(
        agents=[operator],
        tasks=[
            retrieve_the_risk_information_task,
            analyze_the_context_to_take_a_decision_task,
        ],
        process=Process.sequential,
        verbose=True,
    )

    output = crew.kickoff(
        inputs={
            "CO2_CONCENTRATION": params.co2_concentration,
            "LUMINOSITY": params.luminosity_at_tunnel_exit,
        },
    )

    return TunnelOperationResponse.model_validate(output.json_dict)
