"""
Community feed endpoints — real data from the community_stats table.
"""
from flask import jsonify
from app.routes import community_bp
from app.models.community_stats import CommunityStats


@community_bp.route('/feed', methods=['GET'])
def get_community_feed():
    """Return all community vulnerability statistics, sorted by frequency."""
    try:
        stats = (
            CommunityStats.query
            .order_by(CommunityStats.occurrence_count.desc())
            .limit(20)
            .all()
        )
        feed = [
            {
                'vulnerability_type': s.vulnerability_type,
                'severity': s.severity,
                'occurrence_count': s.occurrence_count,
                'last_updated': s.last_updated.isoformat() if s.last_updated else None,
            }
            for s in stats
        ]
        return jsonify({'feed': feed}), 200

    except Exception as exc:
        print(f"Community feed error: {exc}")
        return jsonify({'error': 'Failed to fetch community feed'}), 500


@community_bp.route('/trending', methods=['GET'])
def get_trending():
    """Return the top 10 most frequently seen vulnerabilities."""
    try:
        trending = (
            CommunityStats.query
            .order_by(CommunityStats.occurrence_count.desc())
            .limit(10)
            .all()
        )
        result = [
            {
                'vulnerability_type': t.vulnerability_type,
                'severity': t.severity,
                'occurrence_count': t.occurrence_count,
            }
            for t in trending
        ]
        return jsonify({'trending': result}), 200

    except Exception as exc:
        print(f"Trending error: {exc}")
        return jsonify({'error': 'Failed to fetch trending data'}), 500
