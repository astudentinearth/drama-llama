"""
Usage examples for database CRUD operations.
This file demonstrates how to use the database functions.
"""

from db_config import (
    get_db_context,
    # Session operations
    create_session,
    get_session,
    get_sessions_by_user,
    update_session,
    # Roadmap operations
    create_roadmap,
    get_roadmap_by_session,
    update_roadmap,
    # Goal operations
    create_goal,
    get_goals_by_roadmap,
    mark_goal_started,
    mark_goal_completed,
    update_goal_progress,
    # Learning material operations
    create_learning_material,
    get_materials_by_goal,
    mark_material_completed,
    # User skill operations
    create_user_skill,
    get_user_skills,
    upsert_user_skill,
    bulk_create_user_skills,
    # Complex queries
    get_session_with_full_roadmap,
    get_user_progress_stats,
    get_next_incomplete_goal,
)

from models.db_models import (
    SessionStatusEnum,
    RoadmapStatusEnum,
    SkillLevelEnum
)


def example_create_complete_learning_session():
    """Example: Create a complete learning session with roadmap, goals, and materials."""
    
    with get_db_context() as db:
        # 1. Create a new session for a user
        session = create_session(
            db,
            user_id=123,
            session_name="Full Stack Web Development Journey",
            description="Learning path from backend to frontend development"
        )
        print(f"Created session: {session.id}")
        
        # 2. Create a roadmap for the session
        roadmap = create_roadmap(
            db,
            session_id=session.id,
            user_request="I want to become a full-stack web developer",
            user_summarized_cv="5 years Python experience, basic JavaScript",
            user_expertise_domains=["Python", "Data Analysis"],
            total_estimated_weeks=24,
            graduation_project="Build a full-stack e-commerce platform",
            graduation_project_title="E-Commerce Platform",
            graduation_project_requirements=[
                "User authentication",
                "Product catalog",
                "Shopping cart",
                "Payment integration",
                "Admin dashboard"
            ],
            graduation_project_estimated_hours=80
        )
        print(f"Created roadmap: {roadmap.id}")
        
        # 3. Create goals for the roadmap
        goals_data = [
            {
                "goal_number": 1,
                "title": "Master Advanced JavaScript",
                "description": "Learn ES6+, async/await, promises, and modern JavaScript patterns",
                "priority": 5,
                "skill_level": SkillLevelEnum.INTERMEDIATE,
                "estimated_hours": 40,
                "prerequisites": ["Basic JavaScript"]
            },
            {
                "goal_number": 2,
                "title": "Learn React Fundamentals",
                "description": "Understand components, hooks, state management, and React ecosystem",
                "priority": 5,
                "skill_level": SkillLevelEnum.INTERMEDIATE,
                "estimated_hours": 60,
                "prerequisites": ["Advanced JavaScript", "HTML/CSS"]
            },
            {
                "goal_number": 3,
                "title": "Backend API Development with Node.js",
                "description": "Build RESTful APIs with Express.js and database integration",
                "priority": 4,
                "skill_level": SkillLevelEnum.INTERMEDIATE,
                "estimated_hours": 50,
                "prerequisites": ["JavaScript", "HTTP basics"]
            }
        ]
        
        goals = []
        for goal_data in goals_data:
            goal = create_goal(
                db,
                roadmap_id=roadmap.id,
                **goal_data
            )
            goals.append(goal)
            print(f"Created goal {goal.goal_number}: {goal.title}")
        
        # 4. Add learning materials to the first goal
        materials_data = [
            {
                "title": "JavaScript: The Advanced Concepts",
                "material_type": "course",
                "description": "Deep dive into JavaScript internals and advanced patterns",
                "source_url": "https://example.com/js-advanced",
                "estimated_time_minutes": 1200,
                "difficulty_level": SkillLevelEnum.INTERMEDIATE,
                "relevance_score": 0.95,
                "quality_score": 0.90,
                "end_of_material_project": "Build a promise-based HTTP client library",
                "project_requirements": [
                    "Implement promise-based API",
                    "Handle errors properly",
                    "Add request/response interceptors"
                ]
            },
            {
                "title": "Understanding Async/Await",
                "material_type": "article",
                "description": "Comprehensive guide to asynchronous JavaScript",
                "source_url": "https://example.com/async-await-guide",
                "estimated_time_minutes": 45,
                "difficulty_level": SkillLevelEnum.INTERMEDIATE,
                "relevance_score": 0.88,
                "quality_score": 0.85
            }
        ]
        
        for material_data in materials_data:
            material = create_learning_material(
                db,
                goal_id=goals[0].id,
                **material_data
            )
            print(f"Created learning material: {material.title}")
        
        return session.id


def example_track_progress():
    """Example: Track user progress through a learning session."""
    
    session_id = 1  # Assume we have a session
    
    with get_db_context() as db:
        # Get the full session with all data
        session = get_session_with_full_roadmap(db, session_id)
        if not session or not session.roadmap:
            print("Session or roadmap not found")
            return
        
        roadmap = session.roadmap
        
        # Get the next incomplete goal
        next_goal = get_next_incomplete_goal(db, roadmap.id)
        if next_goal:
            print(f"Next goal to work on: {next_goal.title}")
            
            # Mark the goal as started
            mark_goal_started(db, next_goal.id)
            print(f"Started working on goal: {next_goal.title}")
            
            # Get learning materials for this goal
            materials = get_materials_by_goal(db, next_goal.id)
            print(f"Found {len(materials)} learning materials")
            
            # Complete a learning material
            if materials:
                mark_material_completed(
                    db,
                    materials[0].id,
                    user_rating=5,
                    user_notes="Excellent resource, learned a lot!"
                )
                print(f"Completed material: {materials[0].title}")
            
            # Update goal progress
            update_goal_progress(
                db,
                next_goal.id,
                completion_percentage=45.0,
                actual_hours_spent=18
            )
            print(f"Updated goal progress to 45%")
        
        # Get overall progress stats
        stats = get_user_progress_stats(db, session.user_id)
        print("\nUser Progress Statistics:")
        print(f"  Total Sessions: {stats['total_sessions']}")
        print(f"  Active Sessions: {stats['active_sessions']}")
        print(f"  Total Goals: {stats['total_goals']}")
        print(f"  Completed Goals: {stats['completed_goals']}")
        print(f"  Total Materials: {stats['total_materials']}")
        print(f"  Completed Materials: {stats['completed_materials']}")
        print(f"  Hours Estimated: {stats['total_hours_estimated']}")
        print(f"  Hours Spent: {stats['total_hours_spent']}")


def example_manage_user_skills():
    """Example: Manage user skills extracted from CV or learned through courses."""
    
    user_id = 123
    
    with get_db_context() as db:
        # Create individual skills
        skill1 = create_user_skill(
            db,
            user_id=user_id,
            skill_name="Python",
            skill_level=SkillLevelEnum.EXPERT,
            confidence_score=0.95,
            source="cv",
            verified=True
        )
        print(f"Created skill: {skill1.skill_name}")
        
        # Bulk create skills from CV parsing
        skills_from_cv = [
            {
                "skill_name": "JavaScript",
                "skill_level": SkillLevelEnum.INTERMEDIATE,
                "confidence_score": 0.80,
                "source": "cv",
                "verified": False
            },
            {
                "skill_name": "React",
                "skill_level": SkillLevelEnum.BEGINNER,
                "confidence_score": 0.70,
                "source": "cv",
                "verified": False
            },
            {
                "skill_name": "SQL",
                "skill_level": SkillLevelEnum.INTERMEDIATE,
                "confidence_score": 0.85,
                "source": "cv",
                "verified": False
            }
        ]
        
        created_skills = bulk_create_user_skills(db, user_id, skills_from_cv)
        print(f"Bulk created {len(created_skills)} skills")
        
        # Update a skill after course completion
        upsert_user_skill(
            db,
            user_id=user_id,
            skill_name="React",
            skill_level=SkillLevelEnum.INTERMEDIATE,
            confidence_score=0.90,
            source="course_completion",
            verified=True
        )
        print("Updated React skill after course completion")
        
        # Get all user skills
        all_skills = get_user_skills(db, user_id)
        print(f"\nUser has {len(all_skills)} skills:")
        for skill in all_skills:
            verified_str = "✓" if skill.verified else "✗"
            print(f"  {verified_str} {skill.skill_name}: {skill.skill_level.value} "
                  f"(confidence: {skill.confidence_score:.0%})")


def example_query_and_filter():
    """Example: Various query and filtering operations."""
    
    user_id = 123
    
    with get_db_context() as db:
        # Get all active sessions for a user
        active_sessions = get_sessions_by_user(
            db,
            user_id=user_id,
            status=SessionStatusEnum.ACTIVE
        )
        print(f"User has {len(active_sessions)} active sessions")
        
        # Get completed goals for a roadmap
        if active_sessions:
            roadmap = get_roadmap_by_session(db, active_sessions[0].id)
            if roadmap:
                all_goals = get_goals_by_roadmap(db, roadmap.id)
                completed_goals = get_goals_by_roadmap(db, roadmap.id, completed_only=True)
                print(f"Roadmap has {len(completed_goals)}/{len(all_goals)} goals completed")
                
                # Get only video materials for first goal
                if all_goals:
                    video_materials = get_materials_by_goal(
                        db,
                        all_goals[0].id,
                        material_type="video"
                    )
                    print(f"Found {len(video_materials)} video materials")
        
        # Get only verified expert-level skills
        expert_skills = get_user_skills(
            db,
            user_id=user_id,
            skill_level=SkillLevelEnum.EXPERT,
            verified_only=True
        )
        print(f"User has {len(expert_skills)} verified expert-level skills")


def example_complete_goal():
    """Example: Complete a goal when all its materials are done."""
    
    goal_id = 1  # Assume we have a goal
    
    with get_db_context() as db:
        goal = get_goal(db, goal_id)
        if not goal:
            print("Goal not found")
            return
        
        # Get all materials for the goal
        materials = get_materials_by_goal(db, goal.id)
        completed_count = sum(1 for m in materials if m.is_completed)
        
        print(f"Goal: {goal.title}")
        print(f"Materials: {completed_count}/{len(materials)} completed")
        
        # If all materials are completed, mark goal as completed
        if materials and completed_count == len(materials):
            mark_goal_completed(db, goal.id)
            print(f"✓ Goal completed!")
            
            # Check if all goals in roadmap are completed
            all_goals = get_goals_by_roadmap(db, goal.roadmap_id)
            all_completed = all([g.is_completed for g in all_goals])
            
            if all_completed:
                # Update roadmap status to completed
                update_roadmap(db, goal.roadmap_id, status=RoadmapStatusEnum.COMPLETED)
                print(f"✓ Roadmap completed!")
                
                # Update session status
                roadmap = get_roadmap(db, goal.roadmap_id)
                if roadmap:
                    update_session(db, roadmap.session_id, status=SessionStatusEnum.COMPLETED)
                    print(f"✓ Session completed!")


if __name__ == "__main__":
    print("=== Database CRUD Examples ===\n")
    
    # Uncomment the examples you want to run:
    
    # print("1. Creating a complete learning session...")
    # example_create_complete_learning_session()
    
    # print("\n2. Tracking progress...")
    # example_track_progress()
    
    # print("\n3. Managing user skills...")
    # example_manage_user_skills()
    
    # print("\n4. Query and filter operations...")
    # example_query_and_filter()
    
    # print("\n5. Completing a goal...")
    # example_complete_goal()
    
    print("\nUncomment the examples you want to run in the main block!")

