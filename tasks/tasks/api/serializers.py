from rest_framework import serializers

from tasks.models import Task, TaskDetails, Category, Tag


class TaskDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetails
        fields = ('description', 'estimated_hours')


class TaskReadSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    details = TaskDetailsSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'completed', 'priority', 'user', 'category', 'tags', 'details')


class TaskCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False,)
    details = TaskDetailsSerializer(required=False)

    class Meta:
        model = Task
        fields = ('id', 'title', 'completed', 'priority', 'category', 'tags', 'details', 'user')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        details_data = validated_data.pop('details', None)
        tags_data = validated_data.pop('tags', [])
        validated_data.pop('user', None)
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)

        if details_data:
            TaskDetails.objects.create(task=task, **details_data)

        if tags_data:
            task.tags.add(*tags_data)

        return task


class TaskDetailUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDetails
        fields = ('description', 'estimated_hours')
        extra_kwargs = {'description': {'required': False},
                        'estimated_hours': {'required': False, 'allow_null': True},
                        }


class TaskUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=False, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False,)
    details = TaskDetailsSerializer(required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('title', 'completed', 'priority', 'category', 'tags', 'details', 'user')
        read_only_fields = ('id', 'user')
        extra_kwargs = {'title': {'required': False},
                        'completed': {'required': False},
                        'priority': {'required': False},
                        }

    def update(self, instance: Task, validated_data):
        details_data = validated_data.pop('details', None)
        tags_data = validated_data.pop('tags', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data:
            instance.tags.set(tags_data) # type: ignore

        if details_data is not None:
            if hasattr(instance, 'details'):
                instance.details.delete()
            if details_data:
                TaskDetails.objects.create(task=instance, **details_data)
        return instance