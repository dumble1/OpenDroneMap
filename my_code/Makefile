CC = gcc
TARGET = main
OBJS = copy_vertex
COPY_SOURCE = copy_vertex.c
SOURCE = main.c
all : $(TARGET)

$(TARGET) : $(SOURCE) $(OBJS)
	$(CC) -o $@ $(SOURCE)
$(OBJS) : $(COPY_SOURCE)
	$(CC) -o $(OBJS) $(COPY_SOURCE)

clean:
	rm -f $(TARGET) $(OBJS)
