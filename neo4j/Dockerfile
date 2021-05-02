FROM neo4j:latest

COPY start.sh ./
COPY dbConfig.sh ./

RUN chmod +x ./start.sh
RUN chmod +x ./dbConfig.sh

ENTRYPOINT [ "./start.sh" ]
